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

import os
from . import utils, generator, weights_ops
from akida import Model


def convert(model, file_path, input_scaling=(1.0, 0), input_is_sparse=False):
    """
    Simple function to convert a Keras model to an Akida one.
    These steps are performed:

    1) Merge the depthwise+conv layers into a separable_conv one.
    2) Generate an Akida model based on that model.
    3) Convert weights from the Keras model to Akida.

    :param model: a tf.keras model
    :type model: tf.keras.Model
    :param file_path: destination for the akida model
    :type file_path: str
    :param input_scaling: value of the input scaling
    :type input_scaling: 2 elements tuple
    :input_is_sparse: if True, input will be an InputData layer,
                      otherwise it will be InputConvolutional
    :input_is_sparse: bool

    The relationship between Keras and Akida inputs is:

        input_akida = alpha * input_keras + beta

    :return: an Akida model.
    """

    # Useful extension
    yml_ext = '.yml'

    # Create directories
    dir_name, base_name = os.path.split(file_path)
    if base_name:
        file_root, file_ext = os.path.splitext(base_name)
        if not file_ext:
            file_ext = '.fbz'
    else:
        file_root = model.name
        file_ext = '.fbz'

    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Merge separable convolution
    model_sep = utils.merge_separable_conv(model)

    yaml = generator.generate_model(model_sep,
                                      input_scaling,
                                      input_is_sparse=input_is_sparse)

    # Write a first version of the Akida yml file, with no weight in it
    full_yaml_name = os.path.join(dir_name, file_root + yml_ext)
    with open(full_yaml_name, "w") as save_file:
        save_file.write(yaml)

    # Create an Akida instance from the yaml
    ak_inst = Model(full_yaml_name)

    # Convert weights
    weights_ops.convert_weights(model_sep, ak_inst, input_scaling)

    # Save model
    save_path = os.path.join(dir_name, file_root + file_ext)
    ak_inst.save(save_path)

    return ak_inst
