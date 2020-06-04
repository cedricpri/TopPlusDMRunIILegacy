import time
import numpy as np
#from matplotlib import pyplot as plt
from keras.utils import np_utils
import keras.callbacks as cb
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam
from keras.datasets import mnist
import sys
from optparse import OptionParser
from sklearn.preprocessing import StandardScaler
import keras.callbacks as cb
import random

if __name__ == "__main__":

    sdmsingletop = np.genfromtxt('data/dmsingleptop100.txt', delimiter=',')
    sttbar = np.genfromtxt('data/ttbar.txt', delimiter=',')
    sdmttbar = np.genfromtxt('data/ttbardmscalar100.txt', delimiter=',')

    #Randomize the events
    np.random.shuffle(sdmsingletop)
    np.random.shuffle(sttbar)
    np.random.shuffle(sdmttbar)
    
    N = 13000

    ttbar = sttbar[0:N, :]
    dmttbar = sdmttbar[0:N, :]
    dmsingletop = sdmsingletop[0:N, :]

    zeros = np.zeros((np.shape(ttbar)[0], 1))
    ones = np.zeros((np.shape(dmttbar)[0], 1)) + 1
    twos = np.zeros((np.shape(dmsingletop)[0], 1)) + 2

    features_ = np.concatenate((ttbar, dmttbar, dmsingletop))    
    categories_ = np.concatenate((zeros, ones, twos))

    #Let's mix signal and background together to avoid issues
    mix = list(zip(features_, categories_))
    random.shuffle(mix)
    features_, categories_ = zip(*mix)

    scaler = StandardScaler()
    scaler.fit(features_)
    features = scaler.transform(features_)
    nfeatures = np.shape(features)[1]
    categories = np_utils.to_categorical(categories_, num_classes=3)

    print('Compiling Model ... ')
    model = Sequential()
    model.add(Dense(20, input_dim=nfeatures))
    model.add(Activation('relu'))
    #model.add(Dropout(0.4))
    #model.add(Dense(10, kernel_initializer='he'))
    model.add(Dense(15))
    model.add(Activation('relu'))
    #model.add(Dropout(0.4))
    #model.add(Dense(5, kernel_initializer='he'))
    model.add(Dense(10))
    model.add(Activation('relu'))
    #model.add(Dropout(0.4))
    #model.add(Dense(3, kernel_initializer='he'))
    model.add(Dense(3))
    model.add(Activation('softmax'))
    adam = Adam(lr=0.005)
    model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=['accuracy'])

    model.fit(features, categories, epochs=200, batch_size=200, shuffle = True, validation_split=0.5)






