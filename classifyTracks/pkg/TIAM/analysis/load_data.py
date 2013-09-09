import pickle
from TIAM.config import WHICH_EXP

def X():
    return pickle.load(open('../out/{0}/X.pk'.format(WHICH_EXP), 'r'))

def Y():
    return pickle.load(open('../out/{0}/Y.pk'.format(WHICH_EXP), 'r'))

def Y_supervised():
    return pickle.load(open('../out/{0}/Y_supervised.pk'.format(WHICH_EXP), 'r'))

def Y_hmm():
    return pickle.load(open('../out/{0}/Y_hmm.pk'.format(WHICH_EXP), 'r'))

def Y_svm():
    return pickle.load(open('../out/{0}/Y_svm.pk'.format(WHICH_EXP), 'r'))

