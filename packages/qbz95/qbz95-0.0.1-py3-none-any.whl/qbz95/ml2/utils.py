import numpy as np
import pymysql
import psycopg2
import logging
import time
import pandas as pd
import sys
import datetime


from functools import partial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def eval_numerical_gradient(f, x, verbose=False, h=0.00001):
    """Evaluates gradient df/dx via finite differences:
    df/dx ~ (f(x+h) - f(x-h)) / 2h
    Adopted from https://github.com/ddtm/dl-course/ (our ysda course).
    the function is very ingenious
    """
    fx = f(x) # evaluate function value at original point
    grad = np.zeros_like(x)
    # iterate over all indexes in x
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:

        # evaluate function at x+h
        ix = it.multi_index
        oldval = x[ix]
        x[ix] = oldval + h # increment by h
        fxph = f(x) # evalute f(x + h)
        x[ix] = oldval - h
        fxmh = f(x) # evaluate f(x - h)
        x[ix] = oldval # restore

        # compute the partial derivative with centered formula
        grad[ix] = (fxph - fxmh) / (2 * h) # the slope
        if verbose:
            print (ix, grad[ix])
        it.iternext() # step to next dimension

    return grad


# from preprocessed_mnist import load_dataset
def load_dataset(data_path="../../../data", flatten=False):
    f = np.load(data_path + "/mnist/mnist.npz")
    X_train, y_train = f['x_train'], f['y_train']
    X_test, y_test = f['x_test'], f['y_test']

    # normalize x
    X_train = X_train.astype(float) / 255.
    X_test = X_test.astype(float) / 255.

    # we reserve the last 10000 training examples for validation
    X_train, X_val = X_train[:-10000], X_train[-10000:]
    y_train, y_val = y_train[:-10000], y_train[-10000:]

    if flatten:
        X_train = X_train.reshape([X_train.shape[0], -1])
        X_val = X_val.reshape([X_val.shape[0], -1])
        X_test = X_test.reshape([X_test.shape[0], -1])

    return X_train, y_train, X_val, y_val, X_test, y_test


def iterate_minibatches(X, Y, batch_size, shuffle=False):
    assert len(X) == len(Y)
    if shuffle:
        indices = np.random.permutation(len(X))
    for start_idx in range(0, len(X) - batch_size + 1, batch_size):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batch_size]
        else:
            excerpt = slice(start_idx, start_idx + batch_size)
        yield X[excerpt], Y[excerpt]


def onehot(y, depth=10):
    return np.eye(depth)[y]


def plot_epochs(history, metrics_name):

    train_metrics = history.history[metrics_name]
    val_metrics = history.history['val_'+metrics_name]

    epochs = range(1, len(train_metrics) + 1)

    plt.clf()   # clear figure
    plt.plot(epochs, train_metrics, 'b', label='Training ' + metrics_name, )
    plt.plot(epochs, val_metrics, 'r', label='Validation ' + metrics_name)
    plt.title('Training and validation ' +  metrics_name)
    plt.xlabel('Epochs')
    plt.ylabel(metrics_name)
    plt.legend()

    plt.show()


def plot_tsne(model, perplexity=40, init='pca', n_iter=2500, random_state=23, verbose=0):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=perplexity, n_components=2, init=init, n_iter=n_iter, random_state=random_state, verbose=verbose)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


class ProgressCounter:
    def __init__(self, total_count, step=0, name=''):
        self.total_count = total_count
        self.count = 0
        self.step = step
        self.name = name

    def add_one(self):
        self.count += 1
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if self.step==0 or self.count==self.total_count or self.count % self.step == 0 :
            sys.stdout.write('%s: %s %d/%d\r' % (current_time, self.name, self.count, self.total_count))

class TaskTime:
    def __init__(self, task_name, show_start=False):
        self.show_start = show_start
        self.task_name = task_name
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time()-self.start_time

    def __enter__(self):
        if self.show_start:
            logging.info('start {}'.format(self.task_name))
        return self;

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info('finish {} [elapsed time: {:.2f} seconds]'.format(self.task_name, self.elapsed_time()))



class MySqlHelper:

    @classmethod
    def get_connection(cls, host='15.15.165.218', port=3306, user='grid', password='grid' ):
        """
        :return: return the pre-connect database
        """
        connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             port=port,
                             charset='utf8', #'utf8mb4'
                             use_unicode=True,)
        return connection


class RedshiftHelper:

    @classmethod
    def get_connection(cls, host='15.15.165.218', port=5439, user='grid', password='grid', dbname='csdw'):
        """
        :return: return the pre-connect database
        """
        logging.info('host={}, user={}, port={}, dbname={}'.format(host, user, port, dbname))
        connection = psycopg2.connect(host=host,
                                      user=user,
                                      password=password,
                                      port=port,
                                      dbname=dbname)
        connection.autocommit = True
        return connection

    @classmethod
    def execute(cls, conn, sqls):
        with conn.cursor() as cursor:
            for sql in sqls:
                print('-' * 100)
                logging.info('execute ' + sql)
                cursor.execute(sql)


    @classmethod
    def execute_file(cls, conn, files):
        with conn.cursor() as cursor:
            for file in files:
                print('-' * 100)
                logging.info('execute ' + file)
                with open(file, 'r') as f:
                    sql = f.read()
                cursor.execute(sql)


class PandasHelper:

    @classmethod
    def read_sql(cls, sql, conn, data_set_name='data'):
        with TaskTime('loading {} from database'.format(data_set_name)):
            df = pd.read_sql(sql, conn)
        logging.info('{} records are loaded'.format(len(df)))
        return df

    @classmethod
    def read_csv(cls, path, header=None, columns=None, parse_dates=None, dtype=None, quoting=0, sep='\t', compression='infer'):
        with TaskTime('loading csv from ' + path):
            if header is None:
                df = pd.read_csv(path, sep=sep, header=None, names=columns, dtype=dtype, quoting=quoting,
                                 parse_dates=parse_dates, compression=compression)
            else:
                df = pd.read_csv(path, sep=sep, header=header, names=None, dtype=dtype, quoting=quoting,
                                 parse_dates=parse_dates, compression=compression)
        logging.info('{} records are loaded'.format(len(df)))
        return df

    @classmethod
    def to_csv(cls, df, path, header=False, index=False, sep='\t', compression=None):
        with TaskTime('saving data frame to {}'.format(path)):
            df.to_csv(path, header=header, index=index, sep=sep, compression=compression)
        logging.info('{} records are saved'.format(len(df)))



