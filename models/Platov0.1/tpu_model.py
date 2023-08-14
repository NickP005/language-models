"""
This code is used to train the model on TPU

The sequential model is composed by:
256 TOKENS(14009) INPUT
Embedding layer (200)
200 BiLSTM layer
200 LSTM layer
Dropout 15%
200 Dense layer
14009 Dense categorical_crossentropy OUTPUT
"""
import os
import numpy as np
from keras.layers import Embedding, LSTM, Dropout, Dense, Bidirectional
from keras.models import Sequential, load_model
from keras.optimizers import Adam, SGD
from keras.utils import to_categorical
from keras.utils import plot_model
import tensorflow as tf
import random as rn

def generate_tpu_model(save=True):
    model = Sequential()
    model.add(Embedding(14009, 200, input_length=256))
    model.add(Bidirectional(LSTM(200, return_sequences=True)))
    model.add(LSTM(200, return_sequences=False))
    model.add(Dropout(0.15))
    model.add(Dense(200, activation="relu"))
    model.add(Dense(14009, activation="softmax"))
    #model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.001), metrics=["accuracy"])
    # use SGD optimizer
    model.compile(loss="categorical_crossentropy", optimizer=SGD(lr=0.01, momentum=0.9), metrics=["accuracy"])

    if save:
        model.save('tpu_model.h5')
    return model

# Plot the model
def plot_tpu_model_local(model=None):
    if model is None:
        model = load_model('tpu_model.h5')
    model.summary()
    # plot model high quality svg
    plot_model(model, to_file='model.svg', show_shapes=True, show_layer_names=True, dpi=96)

def delete_train_data():
    files = os.listdir('train_data/')
    for file in files:
        if not file.endswith('.npy'):
            continue
        os.remove('train_data/' + file)

# train tpu model from the sequence files located in train_data/ npy files
def train_tpu_model(tpu_model=None, epochs=10, batch_size=32, save=True):
    if tpu_model is None:
        tpu_model = load_model('tpu_model.h5')
    # for file in train_data do the training process (to avoid excessive memory consumption)
    # read the files in random order each once
    files = os.listdir('train_data/')
    rn.shuffle(files)
    for file in files:
        if not file.endswith('.npy'):
            continue
        print('Training on file: ' + file)
        # load the sequences from the file
        sequences = np.load('train_data/' + file)
        # split the sequences in input and output
        X, y = sequences[:, :-1], sequences[:, -1]
        # convert the output to categorical
        y = to_categorical(y, num_classes=14009)
        # fit the model for tpu
        tpu_model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)
        print("Saving model...")
        tpu_model.save('tpu_model.h5')
        print("model saved!")

    if save:
        tpu_model.save('tpu_model.h5')
        