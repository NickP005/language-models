"""
This file creates the model based on Functional API and saves it to model.h5

The model is composed by:
256 TOKENS(14009) INPUT  
Embedding layer
12 TOKENS(101) INPUT
Embedding layer
180 LSTM layer  
CONCATENATE (INPUT and INPUT2)
180 BiLSTM layer  
DROPOUT 15%  
180 Dense layer | 101 Dense categorical_crossentropy OUTPUT  
14009 Dense categorical_crossentropy OUTPUT

"""
import os
import numpy as np
from keras.layers import Input, Embedding, LSTM, Dropout, Dense, Bidirectional, Concatenate, Reshape
from keras.models import Model, load_model
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.utils import plot_model
import pydot
from train_data import get_sequences_from_dialogue, test_model

def generate_model():
    input_words = Input(shape=(256,))
    input_chars = Input(shape=(12,))

    embedding_words = Embedding(14009, 180, input_length=256)(input_words)
    lstm_words = LSTM(180, return_sequences=True)(embedding_words)
    embedding_chars = Embedding(101, 180, input_length=12)(input_chars)
    lstm_chars = LSTM(180, return_sequences=True)(embedding_chars)

    # Concatenate along the time step axis (axis=1)
    concat = Concatenate(axis=1)([lstm_words, lstm_chars])
    
    # Set return_sequences=False for the Bidirectional LSTM
    bilstm = Bidirectional(LSTM(180, return_sequences=False))(concat)
    #reshape = Reshape((360,))(bilstm)
    dropout = Dropout(0.15)(bilstm)

    dense1 = Dense(180, activation="relu")(dropout)

    # Output layers with the correct shapes
    dense2 = Dense(101, activation="softmax")(dense1)
    dense3 = Dense(14009, activation="softmax")(dense1)

    model = Model(inputs=[input_words, input_chars], outputs=[dense2, dense3])
    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.001), metrics=["accuracy"])
    return model


# Plot the model
def plot_model_local(model=None):
    if model is None:
        model = load_model('model.h5')
    model.summary()
    # plot model high quality svg
    plot_model(model, to_file='model.png', dpi=300, 
               show_shapes=True, show_layer_names=True,
               show_dtype=True, expand_nested=True, rankdir='TB')

# Train the model to predict dense 3
def train_model_words(model=None, epochs=1, batch_size=32):
    if model is None:
        model = load_model('model.h5')

    sequences_words = get_sequences_from_dialogue("Teagete.txt", 0, 30)
    X_words = np.array([sequence[:-1] for sequence in sequences_words])
    y_words = np.array([sequence[-1] for sequence in sequences_words])
    y_words = to_categorical(y_words, num_classes=14009)

    # for the chars, X is just 12 0 ints, y is a random int
    X_chars = np.zeros((len(X_words), 12))
    y_chars = np.random.randint(0, 101, size=(len(X_words),))
    y_chars = to_categorical(y_chars, num_classes=101)

    # Train model to fit y_chars for dense2
    model.compile(loss={"dense_1": "categorical_crossentropy", "dense_2": "categorical_crossentropy"},
                  optimizer=Adam(lr=0.001),
                  metrics=["accuracy"],
                  loss_weights={"dense_1": 0.0, "dense_2": 1.0})
    
    model.fit([X_words, X_chars], {"dense_1": y_chars, "dense_2": y_words}, epochs=epochs, batch_size=batch_size)
    
    model.save("model.h5")

# try the model
def try_model(book_name, character_name, question):
    model = load_model('model.h5')
    word_sequence = test_model(book_name, character_name, question)

    # predict the next 50 words
    for _ in range(50):
        X_words = np.array([word_sequence])
        #X chars are 12 arrays
        X_chars = np.zeros((1, 12))
        y_words = model.predict([X_words, X_chars])
        word_sequence.append(np.argmax(y_words))
    

    return word_sequence



if __name__ == "__main__":
    train_model_words(epochs=1, batch_size=32)
    """
    model = generate_model()
    plot_model_local(model)
    #save
    model.save("model.h5")
    """