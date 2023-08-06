import json
import os
import numpy as np

from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from keras.engine import Input
from keras.layers import Embedding, merge
from keras.models import Model

# tokenizer: can change this as needed
tokenize = lambda x: simple_preprocess(x)


def create_embeddings(data_dir,
                      embeddings_path='embeddings.npz',
                      vocab_path='map.json',
                      **params):
    """
    Generate embeddings from a batch of text
    :param embeddings_path: where to save the embeddings
    :param vocab_path: where to save the word-index map
    """

    class SentenceGenerator(object):
        def __init__(self, dirname):
            self.dirname = dirname

        def __iter__(self):
            for fname in os.listdir(self.dirname):
                for line in open(os.path.join(self.dirname, fname)):
                    yield tokenize(line)

    sentences = SentenceGenerator(data_dir)

    model = Word2Vec(sentences, **params)
    weights = model.syn0
    np.save(open(embeddings_path, 'wb'), weights)

    vocab = dict([(k, v.index) for k, v in model.vocab.items()])
    with open(vocab_path, 'w') as f:
        f.write(json.dumps(vocab))