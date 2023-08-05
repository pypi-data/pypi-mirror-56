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
Functions to convert weights from Keras to Akida.
"""
import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as layers
from cnn2snn import quantization_layers as qlayers
import akida


class WeightsConverter:
    """
    Utility that maps a pre-processed, verified keras model with an Akida
    layer and provides a convert method to set Akida weights to obtain
    equivalent results
    """
    def __init__(self, model, ak_inst, input_scaling=(1.0, 0)):
        self.model = model
        self.ak_inst = ak_inst
        self.alpha = input_scaling[0]
        self.beta = input_scaling[1]
        # List of all matching layers
        self.layer_names = [layer.name for layer in model.layers]

    def _batchnorm_coefficients(self, klayer):
        bn_weights = klayer.get_weights()

        gamma = bn_weights[0]
        beta = bn_weights[1]
        eps = klayer.epsilon
        sigma = np.sqrt(bn_weights[3] + eps)
        mu = bn_weights[2]
        return gamma, beta, sigma, mu

    def _get_threshold(self, index, ak_layer, delta, bias, alpha,\
                       beta_wq_akida=0):
        """calculate threshold and threshold step parameters according to
        the information in the layers that follow the layer that contain the
        weights, using information from global average pooling, batch
        normalization and quantized activation layers.
        """
        # Global average pooling could introduce a scale factor
        gap_rescale = 1
        # step shape can be initialized to match Akida's threshold shape, to it
        # will be correct even if is 0.
        threshold_shape = ak_layer.get_variable('threshold_fire').shape
        step = np.zeros(threshold_shape)
        t0_k = np.zeros(threshold_shape)
        # Pick batchnorm parameters that won't modify the conversion, if no
        # batchnorm layer is present.
        gamma_bn = sigma = np.ones(threshold_shape)
        beta_bn = mu = np.zeros(threshold_shape)
        # Next layer might use a different scale factor
        next_alpha = alpha
        # Start looping searching for the activation in Keras, to retrieve the
        # scale factors.
        for i in range(index + 1, len(self.model.layers)):
            klayer = self.model.layers[i]

            if isinstance(klayer, layers.GlobalAveragePooling2D):
                # If there was a global average pooling, threshold and
                # threshold step should be rescaled by the area because Akida
                # does a simple sum instead of a real average.
                shape = klayer.input_shape
                gap_rescale = int(shape[1]) * int(shape[2])
                continue
            # Activation is the last keras layer that maps on the current Akida
            # layer, so set the activation parameters and exit the loop.
            if isinstance(klayer, qlayers.ActivationDiscreteRelu):
                step += klayer.step
                t0_k = klayer.t0_k
                # update alpha value for next layer
                next_alpha = klayer.scale_factor
                break
            if isinstance(klayer, layers.BatchNormalization):
                # retrieve batchnorm coefficients
                bn_coeffs = self._batchnorm_coefficients(klayer)
                (gamma_bn, beta_bn, sigma, mu) = bn_coeffs
            # If another layer is found, stop looping
            weights_layers = (qlayers.QuantizedConv2D,
                              qlayers.QuantizedDense,
                              qlayers.QuantizedSeparableConv2D)
            if isinstance(klayer, weights_layers):
                break

        # Quantized bias:
        bq = np.round(alpha * delta * bias) / (alpha * delta)

        scale = alpha * delta
        sigma_gamma = (sigma / gamma_bn)
        gamma_sign = np.sign(gamma_bn)

        # Calculate threshold fire and threshold fire step:
        th_fire = scale * gamma_sign * \
            (sigma_gamma * (t0_k - beta_bn) + mu - bq)
        th_fire += beta_wq_akida
        th_fire = np.floor(th_fire * gap_rescale)
        th_fire = th_fire.astype(np.int32)

        th_step = (scale * sigma_gamma * step * gap_rescale).astype(np.float32)

        return th_fire, th_step, next_alpha

    def _convert_separable_conv_weights(self, index, ak_layer, alpha):
        if self.beta != 0:
            raise RuntimeError(f"Layer {ak_layer.name}: unsupported scale "
                               "with beta value different of 0 in separable "
                               "conv")
        klayer = self.model.layers[index]
        dw_weights = klayer.get_weights()[0]
        pw_weights = klayer.get_weights()[1]
        if klayer.use_bias:
            bias = klayer.get_weights()[2]
        else:
            bias = 0

        # quantize weights:
        dwwq, delta_dw = quantize_weights(klayer.quantizer, dw_weights)
        pwwq, delta_pw = quantize_weights(klayer.quantizer, pw_weights)

        # Transpose Keras weights to (W, H, C, N) to match Akida shape
        dwwq = dwwq.transpose((1, 0, 2, 3))
        # Set each slice (flipped on W and H) per neuron. Multiply times delta.
        dwwq_akida = np.flip(dwwq, axis=(0,1)) * delta_dw
        dwwq_akida = np.round(dwwq_akida).astype(np.int8)

        # Pointwise weights in Keras have HWCN format and H = W = 1. This
        # makes the conversion to Akida's NCHW trivial (just transpose).
        pwwq_akida = pwwq * delta_pw
        pwwq_akida = np.round(pwwq_akida).astype(np.int8)

        # For separable, delta can be seen as the product of the delta of the
        # two convolutions.
        delta = delta_dw * delta_pw

        # Finally set variables for this layer
        ak_layer.set_variable("weights", dwwq_akida)
        ak_layer.set_variable("weights_pw", pwwq_akida)
        # Set threshold variables if necessary
        if "threshold_fire" in ak_layer.get_variable_names():
            # Calcultate threshold parameters
            (th_fire, th_step, alpha) = self._get_threshold(
                index, ak_layer, delta, bias, alpha)
            ak_layer.set_variable("threshold_fire", th_fire)
            ak_layer.set_variable("threshold_fire_step", th_step)
        return alpha

    def _convert_dense_weights(self, index, ak_layer, alpha):
        if self.beta != 0:
            raise RuntimeError(f"Layer {ak_layer.name}: unsupported scale "
                               "with beta value different of 0 in conv")
        klayer = self.model.layers[index]
        weights = klayer.get_weights()[0]
        if klayer.use_bias:
            bias = klayer.get_weights()[1]
        else:
            bias = 0

        # quantize weights:
        wq, delta = quantize_weights(klayer.quantizer, weights)

        # retrieve input dimensions from Akida's layer
        inwidth, inheight, inchans = ak_layer.input_dims
        # Kernels in the fully connected are in the (HxWxC,N) format, more
        # specifically in each neuron data is laid out in the H,W,C format. In
        # Akida we expect a kernel in the (N,CxHxW,1,1), where the data in each
        # neuron is laid out in the W,H,C format as the input dimensions are
        # set.
        # So the operations done in order to obtain the akida fully connected
        # kernel are:
        # 1. reshape to H,W,C,N to split data across dimensions
        # 2. transpose dimensions to obtain C,H,W,N
        # 3. reshape to: 1,1,CxHxW,N
        #
        wq_akida = wq.reshape(inheight, inwidth, inchans, klayer.units) \
            .transpose(2, 0, 1, 3) \
            .reshape(1, 1, inchans * inheight * inwidth, klayer.units)
        # Multiply by delta, round and cast to int
        wq_akida = wq_akida * delta
        wq_akida = np.round(wq_akida)
        wq_akida = wq_akida.astype(np.int8)

        # Finally set variables for this layer
        ak_layer.set_variable("weights", wq_akida)
        # Set threshold variables if necessary
        if "threshold_fire" in ak_layer.get_variable_names():
            # Calcultate threshold parameters
            (th_fire, th_step, alpha) = self._get_threshold(
                index, ak_layer, delta, bias, alpha)
            ak_layer.set_variable("threshold_fire", th_fire)
            ak_layer.set_variable("threshold_fire_step", th_step)
        return alpha

    def _convert_conv_weights(self, index, ak_layer, alpha):
        klayer = self.model.layers[index]
        weights = klayer.get_weights()[0]
        if klayer.use_bias:
            bias = klayer.get_weights()[1]
        else:
            bias = 0

        # quantize weights:
        wq, delta = quantize_weights(klayer.quantizer, weights)

        # Transpose weights to get from HWCN to WHCN used in Akida
        # and multiply times scale factor and input scale for Akida
        wq_akida = np.transpose(wq, axes=[1, 0, 2, 3]) * delta
        wq_akida = np.round(wq_akida)
        wq_akida = wq_akida.astype(np.int8)
        # Flip W and H in akida's kernel if layer is not input convolutional
        ak_layer_type = ak_layer.parameters.layer_type
        if ak_layer_type != akida.core.InputConvolutional:
            wq_akida = np.flip(wq_akida, axis=[0, 1])

        # To quantize beta, it needs to be multiplied by the convolution of an
        # identity multiplied by the quantized weights. To do that in a simple
        # way, beta could be multiplied with the sum of weights.
        if self.beta != 0:
            beta_wq_akida = np.sum(wq_akida, axis=(0, 1, 2)) * self.beta
        else:
            beta_wq_akida = 0.0

        # Finally set variables for this layer
        ak_layer.set_variable("weights", wq_akida)
        # Set threshold variables if necessary
        if "threshold_fire" in ak_layer.get_variable_names():
            # Calcultate threshold parameters
            (th_fire, th_step, alpha) = self._get_threshold(
                index, ak_layer, delta, bias, alpha, beta_wq_akida)
            ak_layer.set_variable("threshold_fire", th_fire)
            ak_layer.set_variable("threshold_fire_step", th_step)

        # Set beta to 0, now that it has been taken into account
        self.beta = 0
        return alpha

    def _get_layer_index(self, name):
        """
        Return index of keras layer with given name
        """
        for i in range(len(self.model.layers)):
            if self.model.layers[i].name == name:
                return i
        raise RuntimeError(f"Could not find layer name {name} in the Keras"
                           "model.")

    def convert(self):
        """
        Main weight converter method, will loop through layers and set
        weights in akida's layers
        """
        # The scale factor for the next layer
        alpha = self.alpha
        layer_count = self.ak_inst.get_layer_count()
        for i in range(layer_count):
            ak_layer = self.ak_inst.get_layer(i)
            # Check if layer name matches
            if ak_layer.name in self.layer_names:
                index = self._get_layer_index(ak_layer.name)
                klayer = self.model.layers[index]
                if isinstance(klayer, qlayers.QuantizedConv2D):
                    alpha = self._convert_conv_weights(index, ak_layer, alpha)
                    continue
                if isinstance(klayer, qlayers.QuantizedSeparableConv2D):
                    alpha = self._convert_separable_conv_weights(index, ak_layer, alpha)
                    continue
                if isinstance(klayer, qlayers.QuantizedDense):
                    alpha = self._convert_dense_weights(index, ak_layer, alpha)
                    continue
        return self.ak_inst


def convert_weights(model, ak_inst, input_scaling=(1.0, 0)):
    """
    This function converts weights from the Keras model to the Akida model
    by applying the necessary conversions.

    :param model: tf.keras model containing the original weights
    :type model: tf.keras.Model
    :param ak_inst: destination model, where the weights are going to be set
    :param input_scaling: value of the input scaling
    :type input_scaling: 2 elements tuple

    :return: the modified akida model.
    """
    if not tf.executing_eagerly():
        raise SystemError ("Tensorflow eager execution is disabled. "
                           "It is required to convert Keras weights to Akida.")
    converter = WeightsConverter(model, ak_inst, input_scaling)
    return converter.convert()
    
def quantize_weights(quantizer, w):
    """
    Returns quantized weights and delta as numpy arrays.
    Internally, it uses a tf.function that wraps calls to the quantizer in
    a graph, allowing the weights to be quantized eagerly.

    :param quantizer: the quantizer object
    :param w: the weights to quantize
    :type quantizer: a `WeightQuantizer`
    :type w: a `np.ndarray`
    :return: the quantized weights `np.ndarray` and the scale factor scalar
    """
    # Helper function to return quantized weights and scale factor
    def quantize(quantizer, w):
        return quantizer.quantize(w), quantizer.scale_factor(w)
    # Wrap quantize helper in a graph to execute it eagerly
    quantize_wrapper = tf.function(quantize)
    # Invoke wrapper with a constant Tensor initialized from the weights
    wq, delta = quantize_wrapper(quantizer, tf.constant(w))
    # Return eager tensors as numpy arrays
    return wq.numpy(), delta.numpy()
