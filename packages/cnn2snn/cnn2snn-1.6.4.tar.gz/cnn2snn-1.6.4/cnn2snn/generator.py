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
"""
Parsing functions that are able to generate an Akida model from a keras model.
"""
import tensorflow.keras.layers as layers
from . import quantization_layers as qlayers

from akida import (Model, Convolutional, FullyConnected,
                   SeparableConvolutional, InputData, InputConvolutional,
                   ConvolutionMode, PoolingType)


def _get_convolution_mode(str_conv_mode):
    if str_conv_mode == 'same':
        return ConvolutionMode.Same
    else:
        return ConvolutionMode.Valid


def _parse_input_conv(layer, current):
    if not isinstance(layer, qlayers.QuantizedConv2D):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedConv2D")
    current["layerType"] = "inputConvolutional"
    current["convolution_mode"] = _get_convolution_mode(layer.padding)
    current["kernel_height"] = layer.kernel_size[0]
    current["kernel_width"] = layer.kernel_size[1]
    current["num_neurons"] = int(layer.kernel.shape[3])
    current["weights_bits"] = layer.quantizer.bitwidth
    current["input_channels"] = int(layer.input_shape[3])
    current["stride_x"] = layer.strides[1]
    current["stride_y"] = layer.strides[0]
    current["name"] = layer.name


def _parse_conv(layer, current):
    dw_conv = qlayers.QuantizedDepthwiseConv2D
    if not isinstance(layer, qlayers.QuantizedConv2D) \
            or isinstance(layer, dw_conv):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedConv2D")
    if layer.strides != (1,1):
        raise ValueError(f"Layer {layer.name} must have strides of (1,1). "
                        f"Received strides of {layer.strides}.")
    current["layerType"] = "convolutional"
    current["convolution_mode"] = _get_convolution_mode(layer.padding)
    current["kernel_height"] = layer.kernel_size[0]
    current["kernel_width"] = layer.kernel_size[1]
    current["num_neurons"] = int(layer.kernel.shape[3])
    current["weights_bits"] = layer.quantizer.bitwidth
    current["name"] = layer.name


def _parse_separable_conv(layer, current):
    if not isinstance(layer, qlayers.QuantizedSeparableConv2D):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedSeparableConv2D")
    current["layerType"] = "separableConvolutional"
    current["convolution_mode"] = _get_convolution_mode(layer.padding)
    current["kernel_height"] = layer.kernel_size[0]
    current["kernel_width"] = layer.kernel_size[1]
    # num neurons is set to the number of filters of the depthwise
    current["num_neurons"] = int(layer.depthwise_kernel.shape[2])
    current["num_pointwise_neurons"] = int(layer.pointwise_kernel.shape[3])
    current["weights_bits"] = layer.quantizer.bitwidth
    current["name"] = layer.name


def _parse_dense(layer, current):
    if not isinstance(layer, qlayers.QuantizedDense):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedDense")
    current["layerType"] = "fullyConnected"
    current["num_neurons"] = layer.units
    current["weights_bits"] = layer.quantizer.bitwidth
    current["name"] = layer.name


def _parse_max_pooling(layer, current):
    if not isinstance(layer, layers.MaxPooling2D):
        raise TypeError(f"Layer {layer.name} was expected to be MaxPooling2D")
    current["pooling_type"] = PoolingType.Max
    current["pooling_height"] = layer.pool_size[0]
    current["pooling_width"] = layer.pool_size[1]
    current["pooling_stride_y"] = layer.strides[0]
    current["pooling_stride_x"] = layer.strides[1]
    # Check the padding is identical to the one in the convolution
    if current["convolution_mode"] != _get_convolution_mode(layer.padding):
        raise ValueError(f"Layer {layer.name} has a padding {layer.padding},"
                          "which is different from the padding of the related"
                          "convolutional layer")

def _parse_global_average_pooling(layer, current):
    if not isinstance(layer, layers.GlobalAveragePooling2D):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "GlobalAveragePooling2D")
    current["pooling_type"] = PoolingType.Average


def _create_current_akida_layer(current):
    """
    Returns an Akida layer based on the input dictionary containing the
    parameters.
    """
    if current is None or current == {}:
        return

    layer_type = current.pop('layerType')
    if ("threshold_fire_bits" not in current and
            layer_type != "inputData"):
        current["activations_enabled"] = False

    if layer_type == 'inputData':
        layer_ak = InputData(**current)
    elif layer_type == 'inputConvolutional':
        layer_ak = InputConvolutional(**current)
    elif layer_type == 'convolutional':
        layer_ak = Convolutional(**current)
    elif layer_type == 'separableConvolutional':
        layer_ak = SeparableConvolutional(**current)
    elif layer_type == 'fullyConnected':
        layer_ak = FullyConnected(**current)

    current.clear()
    return layer_ak


def generate_model(model, input_scaling, input_is_sparse=False):
    """
    Create an akida model that maps an existing keras model

    :param model: a tf.keras model
    :type model: tf.keras.Model
    :param input_scaling: value of the input scaling, alpha and beta
    :type input_scaling: 2 elements tuple
    :input_is_sparse: if True, input will be an inputData layer,
                      otherwise it will be inputConvolutional
    :input_is_sparse: bool

    The relationship between Keras and Akida inputs is:

        input_akida = alpha * input_keras + beta

    :return: a string with the model in yaml
    """
    for layer in model.layers:
        if hasattr(layer, 'data_format'):
            if layer.data_format == "channels_first":
                raise RuntimeError("unsupported data format channels_first")

    model_ak = Model()

    # Current layer config
    current = {}

    # First we need to map the input layer
    start_layer = 0
    # If first layer is input layer, skip it
    if isinstance(model.layers[0], layers.InputLayer):
        start_layer = 1
    input_layer = model.layers[start_layer]
    beta = input_scaling[1]
    if input_is_sparse:
        if beta != 0:
            raise ValueError(
                "beta should be 0 when input_is_sparse is True.")
        current["layerType"] = "inputData"
        current["input_features"] = int(input_layer.input_shape[3])
        current['name'] = input_layer.name + "_input"
        # We do not set these attributes: packetSize, accumulate.
    else:
        _parse_input_conv(input_layer, current)
        current["padding_value"] = int(beta)
        start_layer += 1
    current["input_height"] = int(input_layer.input_shape[1])
    current["input_width"] = int(input_layer.input_shape[2])

    # Loop on layers
    for i in range(start_layer, len(model.layers)):
        layer = model.layers[i]
        if isinstance(layer, qlayers.QuantizedConv2D):
            model_ak.add(_create_current_akida_layer(current))
            _parse_conv(layer, current)
            continue
        if isinstance(layer, qlayers.QuantizedSeparableConv2D):
            model_ak.add(_create_current_akida_layer(current))
            _parse_separable_conv(layer, current)
            current["name"] = layer.name
            continue
        if isinstance(layer, qlayers.QuantizedDense):
            model_ak.add(_create_current_akida_layer(current))
            _parse_dense(layer, current)
            current["name"] = layer.name
            continue
        # Parse pooling params/layer
        if isinstance(layer, layers.MaxPooling2D):
            if "pooling_type" in current:
                raise RuntimeError(f"Two pooling layers were detected in layer"
                        f" {current['name']}. Only one pooling layer is "
                        f"supported.")
            _parse_max_pooling(layer, current)
            continue
        if isinstance(layer, layers.GlobalAveragePooling2D):
            if "pooling_type" in current:
                raise RuntimeError(f"Two pooling layers were detected in layer"
                        f" {current['name']}. Only one pooling layer is "
                        f"supported.")
            _parse_global_average_pooling(layer, current)
            continue
        if isinstance(layer, qlayers.BaseQuantizedActivation):
            current["threshold_fire_bits"] = layer.bitwidth
        # Allow flatten before a dense layer
        if isinstance(layer, layers.Flatten):
            try:
                if isinstance(model.layers[i+1], qlayers.QuantizedDense):
                    continue
            except IndexError:
                pass
            raise RuntimeError("Flatten layer only supported before a Dense "
                               "one")
        # Allow some other layers useful in keras but that will be discarded
        # or ignored during conversion
        ignore_list = (layers.Activation,
                       layers.Reshape,
                       layers.Dropout,
                       layers.Softmax,
                       layers.BatchNormalization)
        if isinstance(layer, ignore_list):
            continue

        # If you got here it means the layer is not recognised: raise an error.
        raise RuntimeError(f"layer {layer.name}: unsupported type "
                           f"{layer.__class__.__name__}.")

    # Append last parsed layer if any
    model_ak.add(_create_current_akida_layer(current))

    return model_ak
