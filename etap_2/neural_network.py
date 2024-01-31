import config
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU
from config import TARGET, FEATURES
import tensorflow as tf


def createNeuralNetworkModel(layer_size_list, alpha_list):
    model = Sequential()

    for ind, layer_size in enumerate(layer_size_list):
        if ind == 0:
            model.add(Dense(layer_size, input_dim=len(FEATURES),
                      activation=LeakyReLU(alpha=alpha_list[ind])))
            continue
        model.add(
            Dense(layer_size, activation=LeakyReLU(alpha=alpha_list[ind])))
    model.add(Dense(len(TARGET), activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=[tf.keras.metrics.F1Score()])

    return model


def train_neural_network(params, X_train, y_train):
    model = createNeuralNetworkModel(
        params['layer_size_list'], params['alpha_list'])

    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

    return model
