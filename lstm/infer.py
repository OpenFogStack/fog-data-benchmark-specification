# !/usr/bin/env python3
#
# Copyright (c) Tobias Pfandzelter. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import os
import sys
from tensorflow import lite as tflite
import numpy as np

rng = np.random.default_rng(seed=1)
if __name__ == "__main__":
    # read the environment variables
    resolution_byte = int(os.getenv("RESOLUTION_BYTE", "8"))
    resolution_num = int(os.getenv("RESOLUTION_NUM", "3"))
    input_size = int(os.getenv("INPUT_SIZE", "40"))

    # https://www.tensorflow.org/lite/api_docs/python/tf/lite/Interpreter#used-in-the-notebooks

    interpreter = tflite.Interpreter(model_path="./model.tflite")
    interpreter.allocate_tensors()

    print("signature list: %s" % interpreter.get_signature_list())

    fn = interpreter.get_signature_runner('serving_default')

    input_value = np.zeros((input_size, resolution_num), dtype=np.float32)

    while True:
        # get input from stdin until satisfied
        idx = 0
        for line in sys.stdin:
            if idx >= input_size:
                break
            input_value[idx] = [float(i) for i in line.split()]
            idx += 1

        # flatten input
        model_input = input_value.reshape(1, input_value.shape[0]*input_value.shape[1], 1)
        # print(model_input.shape)
        output = fn(x=input_value)

        print(output["output_0"][0][0])
