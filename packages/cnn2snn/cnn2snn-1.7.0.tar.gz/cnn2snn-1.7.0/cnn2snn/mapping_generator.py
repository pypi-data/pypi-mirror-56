#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""Parsing function to generate layers mapping between Keras and Akida.
Two data classes store the mapping: LayerMapping and ModelMapping.

"""
import tensorflow.keras.layers as layers
from . import quantization_layers as qlayers
from akida import LayerType

class LayerMapping:
    """This data class stores the indices of Keras layers that represent a
    single Akida layer. For example, a 'Convolutional' Akida layer corresponds
    to multiple Keras layers:
    - a QuantizedConv2D layer
    - an optional batch normalization layer
    - an optional pooling layer
    - a discrete ReLU activation (optional if last layer)
    """
    def __init__(self, layer_type, index_neural):
        """Creates a layer map of a single Akida layer from Keras layers.

        Args:
            layer_type (:obj:`akida.LayerType`): the type of the Akida layer.
            index_neural (int): the index of the corresponding Keras
                neural layer.

        """
        self.layer_type = layer_type
        self.index_neural = index_neural
        self.index_pool = None
        self.index_batchnorm = None
        self.index_activation = None


class ModelMapping:
    """This data class maps a Keras model to a future Akida model (not built yet).

    When an instance of ModelMapping is created, it will generate a list of
    LayerMapping objects mapping the Keras model with a succession of Akida
    layers.
    A check is then performed to ensure that the Keras model is compatible with
    Akida.

    Note:
        Note that no Akida model is generated at this step: only a mapping is
        created.

    """
    def __init__(self, model_keras, layer_maps):
        self.model_keras = model_keras
        self.layer_maps = layer_maps


def generate_model_mapping(model, input_is_sparse):
    """Generates a model map between Keras and Akida models.

    This function returns a model map from a Keras model. The model map
    corresponds to the Akida layers mapped from the Keras layers.

    Args:
        model (tf.keras model): the model to parse.
        input_is_sparse (bool): if True, input will be an inputData layer,
            otherwise it will be inputConvolutional.

    Returns:
       :obj:`ModelMapping`: a model map corresponding to the input Keras model.

    """
    for layer in model.layers:
        if hasattr(layer, 'data_format'):
            if layer.data_format == "channels_first":
                raise RuntimeError("unsupported data format channels_first")

    layer_maps = []

    # First we need to map the input layer
    first_layer = 0
    # If first layer is input layer, skip it
    if isinstance(model.layers[0], layers.InputLayer):
        first_layer = 1
    # Get first Akida layer
    if input_is_sparse:
        layer_ak = LayerMapping(LayerType.InputData, first_layer)
    else:
        layer_ak = LayerMapping(LayerType.InputConvolutional, first_layer)
        first_layer += 1

    # Loop on layers
    neural_layers = (qlayers.QuantizedConv2D, qlayers.QuantizedSeparableConv2D,
                     qlayers.QuantizedDense)
    ignore_list = (layers.Activation,
                   layers.Reshape,
                   layers.Dropout,
                   layers.Softmax,
                   layers.BatchNormalization)
    for i in range(first_layer, len(model.layers)):
        layer = model.layers[i]
        # If this layer is a neural layer, append the current Akida layer and
        # start a new one
        if isinstance(layer, neural_layers):
            layer_maps.append(layer_ak)

        # Neural layers
        if isinstance(layer, qlayers.QuantizedConv2D):
            layer_ak = LayerMapping(LayerType.Convolutional, i)
        elif isinstance(layer, qlayers.QuantizedSeparableConv2D):
            layer_ak = LayerMapping(LayerType.SeparableConvolutional, i)
        elif isinstance(layer, qlayers.QuantizedDense):
            layer_ak = LayerMapping(LayerType.FullyConnected, i)

        # Pooling + batchnorm + activation layers
        elif isinstance(layer, (layers.MaxPooling2D, layers.GlobalAveragePooling2D)):
            if layer_ak.index_pool:
                raise RuntimeError(f"Two pooling layers were detected in layer"
                        f" {layer_ak.get_neural_layer().name}. Only "
                        f"one pooling layer is supported.")
            layer_ak.index_pool = i
        elif isinstance(layer, layers.BatchNormalization):
            layer_ak.index_batchnorm = i
        elif isinstance(layer, qlayers.BaseQuantizedActivation):
            layer_ak.index_activation = i

        # Allow flatten before a dense layer
        elif isinstance(layer, layers.Flatten):
            try:
                if isinstance(model.layers[i+1], qlayers.QuantizedDense):
                    continue
            except IndexError:
                pass
            raise RuntimeError("Flatten layer only supported before a Dense "
                               "one")
        # Allow some other layers useful in keras but that will be discarded
        # or ignored during conversion
        elif isinstance(layer, ignore_list):
            continue
        else:
            # If you got here it means the layer is not recognised: raise an error.
            raise RuntimeError(f"layer {layer.name}: unsupported type "
                               f"{layer.__class__.__name__}.")

    # Append last parsed layer if any
    layer_maps.append(layer_ak)

    return ModelMapping(model, layer_maps)


def check_mapping_compatibility(model_map):
    """Checks whether the future model will be compatible with Akida.

    This function must mainly test the incompatibities due to the order of the
    layers (parameters of the layers have already been tested at creation of
    the quantized layers).

    """
    layers_k = model_map.model_keras.layers

    # Error if hidden layer without activation
    for layer_map in model_map.layer_maps[:-1]:
        if layer_map.layer_type != LayerType.InputData \
                and not layer_map.index_activation:
            raise RuntimeError("No activation layer detected with layer "
                               f"{layers_k[layer_map.index_neural].name}. "
                               "Activation is required in hidden layers.")

    # Error if bias in the last layer without activation
    layer_map = model_map.layer_maps[-1]
    if not layer_map.index_activation \
            and layers_k[layer_map.index_neural].use_bias:
        raise RuntimeError(f"The last neural layer "
                           f"{layers_k[layer_map.index_neural].name} must"
                           f" not have bias. Set 'use_bias=False'")

	# Error if batch norm in the last layer without activation
    if not layer_map.index_activation \
            and layer_map.index_batchnorm:
        name_BN = layers_k[layer_map.index_batchnorm].name
        raise RuntimeError(f"The last neural layer "
                           f"{layers_k[layer_map.index_neural].name} must not"
                           f" be followed by a batch normalization layer. Here"
                           f", layer {name_BN} is a batch norm layer.")