# !/usr/bin/env python3
#
# Copyright (c) Tobias Pfandzelter. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import os
import sys
import typing

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np

from numpy.random import seed
seed(1)

import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import sklearn.metrics
from numpy import array

RANDOM_DATA_LENGTH = 10_000
TRAINING_SPLIT = 0.8
N_EPOCHS =  1 #5
BATCH_SIZE = 32
LSTM_UNITS = 125
MODEL_SAVE_PATH = "./model.tflite"

if __name__ == "__main__":
    # read the environment variables
    resolution_byte = int(os.getenv("RESOLUTION_BYTE", "8"))
    resolution_num = int(os.getenv("RESOLUTION_NUM", "3"))
    input_size = int(os.getenv("INPUT_SIZE", "40"))

    # create some random data
    train_data_x = np.random.randint(100, size=(int(RANDOM_DATA_LENGTH*TRAINING_SPLIT), input_size, resolution_num))

    # print(train_data_x.shape)

    train_data_y = np.random.randint(100, size=(int(RANDOM_DATA_LENGTH*TRAINING_SPLIT), 1))

    # print(train_data_y.shape)

    test_data_x = np.random.randint(100, size=(int(RANDOM_DATA_LENGTH*(1-TRAINING_SPLIT)), input_size, resolution_num))

    # print(test_data_x.shape)

    test_data_y = np.random.randint(100, size=(int(RANDOM_DATA_LENGTH*(1-TRAINING_SPLIT)), 1))

    # print(test_data_y.shape)

    # flatten input
    train_data_x = train_data_x.reshape(train_data_x.shape[0], train_data_x.shape[1]*resolution_num)
    # print(train_data_x.shape)

    test_data_x = test_data_x.reshape(test_data_x.shape[0], test_data_x.shape[1]*resolution_num)
    # print(test_data_x.shape)

    sc = MinMaxScaler(feature_range = (0, 1))
    # train_data_x = sc.fit_transform(train_data_x.reshape(-1, train_data_x.shape[-1])).reshape(train_data_x.shape)
    train_data_x = sc.fit_transform(train_data_x)
    train_data_y = sc.fit_transform(train_data_y)
    # test_data_x = sc.fit_transform(test_data_x.reshape(-1, test_data_x.shape[-1])).reshape(test_data_x.shape)
    test_data_x = sc.fit_transform(test_data_x)
    test_data_y = sc.fit_transform(test_data_y)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(input_size*resolution_num, 1), name='input'),
        tf.keras.layers.LSTM(LSTM_UNITS, activation='sigmoid', return_sequences=True, input_shape=(train_data_x.shape[1]*resolution_num, 1)),
        tf.keras.layers.LSTM(LSTM_UNITS, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    history = model.fit(train_data_x, train_data_y, epochs=N_EPOCHS, batch_size=BATCH_SIZE)

    run_model = tf.function(lambda x: model(x))

    # This is important, let's fix the input size.
    STEPS = input_size*resolution_num
    INPUT_SIZE = 1
    concrete_func = run_model.get_concrete_function(
        tf.TensorSpec([None, STEPS, INPUT_SIZE], model.inputs[0].dtype))

    # model directory.
    model.save("./model_keras", save_format="tf", signatures=concrete_func)

    converter = tf.lite.TFLiteConverter.from_saved_model("./model_keras")

    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    converter._experimental_lower_tensor_list_ops = False

    tflite_model = converter.convert()

    # converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]
    # converter._experimental_lower_tensor_list_ops = False

    # tflite_model = converter.convert()

    # Save the model.
    with open(MODEL_SAVE_PATH, "wb") as f:
        f.write(tflite_model)

    y_predicted = model.predict(test_data_x)

    #
    # 'De-normalize' the data
    #
    y_predicted_descaled = sc.inverse_transform(y_predicted)
    y_train_descaled = sc.inverse_transform(train_data_y)
    y_test_descaled = sc.inverse_transform(test_data_y)
    y_pred = y_predicted.ravel()
    y_pred = [round(yx, 2) for yx in y_pred]
    y_tested = test_data_y.ravel()

    mse = ((y_test_descaled - y_predicted_descaled)**2).mean(axis=None)
    r2 = sklearn.metrics.r2_score(y_test_descaled, y_predicted_descaled)
    print("mse=" + str(round(mse,2)))
    print("r2=" + str(round(r2,2)))