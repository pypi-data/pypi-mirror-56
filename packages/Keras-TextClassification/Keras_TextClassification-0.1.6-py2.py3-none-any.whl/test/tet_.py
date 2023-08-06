# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2019/11/29 14:23
# @author  : Mo
# @function:


from keras import layers
from keras.layers import Input, Add, Dense,Dropout, Lambda, Concatenate
from keras.layers import Flatten
from keras.optimizers import Adam
from keras.models import Model
import keras.backend as K
def tst_1():
    num_channels = 3
    inputs = Input(shape=(num_channels, 1000, 1))
    branch_outputs = []
    for i in range(num_channels):
        # Slicing the ith channel:
        out = Lambda(lambda x: x[:, i, :, :], name = "Lambda_" + str(i))(inputs)
        # Setting up your per-channel layers (replace with actual sub-models):
        out = Dense(224, activation='relu', name = "Dense_224_" + str(i))(out)
        out = Dense(112, activation='relu', name = "Dense_112_" + str(i))(out)
        out = Dense(56, activation='relu', name = "Dense_56_" + str(i))(out)
        branch_outputs.append(out)
        # Concatenating together the per-channel results:
        out = Concatenate()(branch_outputs)
        dense1 = Dense(224, activation='relu')(out)
        drop1 = Dropout(0.5)(dense1)
        dense2 = Dense(112, activation='relu')(drop1)
        drop2 = Dropout(0.5)(dense2)
        dense3 = Dense(32, activation='relu')(drop2)
        densef = Dense(1, activation='sigmoid')(dense3)
        model = Model(inputs = inputs, outputs = densef)
    return model


Net = tst_1()
Net.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
Net.summary()