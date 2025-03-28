import pickle
import gzip

import numpy as np

def load_data():
    f = gzip.open('../data/mnist.pkl.gz', 'rb')
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    training_data, validation_data, test_data = u.load()
    f.close()
    return (training_data, validation_data, test_data)

def load_data_wrapper():
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (784,1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0])]
    validation_results = [vectorized_result(y) for y  in va_d[1]]
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0])]
    test_results = [vectorized_result(y) for y  in te_d[1]]

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e