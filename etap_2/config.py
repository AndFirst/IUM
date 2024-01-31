import random
import numpy as np
import tensorflow as tf
RANDOM_STATE = 42
AB_DIVIDE_MONTH = 7

FEATURES = ['number_of_advertisements',
            'number_of_skips',
            'number_of_likes',
            'total_tracks_duration_ms',
            'number_of_different_artists',
            'average_release_date',
            'average_duration_ms',
            'explicit_tracks_ratio',
            'average_popularity',
            'average_acousticness',
            'average_danceability',
            'average_energy',
            'average_instrumentalness',
            'average_liveness',
            'average_loudness',
            'average_speechiness',
            'average_tempo',
            'average_valence'
            ]

TARGET = [
    'premium_purchased',
    'premium_purchased_this_month',
]

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)
