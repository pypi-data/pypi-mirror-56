import tensorflow as tf
import keras
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            embeddings_initializer=Constant(embedding_matrix),
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences


import pandas as pd
df = pd.read_csv()
df.mean

from scipy import optimize
optimize.fmin_slsqp
from scipy.optimize import minimize
