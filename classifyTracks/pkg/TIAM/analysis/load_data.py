import cPickle
from TIAM.config import WHICH_EXP

def X():
    return cPickle.load(open('../out/{0}/X.pk'.format(WHICH_EXP), 'r'))

def Y_supervised():
    return cPickle.load(open('../out/{0}/Y_supervised.pk'.format(WHICH_EXP), 'r'))

def Y_proc():
    return cPickle.load(open('../out/{0}/Y_proc.pk'.format(WHICH_EXP), 'r'))

def Y_hmm():
    return cPickle.load(open('../out/{0}/Y_hmm.pk'.format(WHICH_EXP), 'r'))

def Y_svm():
    return cPickle.load(open('../out/{0}/Y_svm.pk'.format(WHICH_EXP), 'r'))

def Y_dtree():
    return cPickle.load(open('../out/{0}/Y_dtree.pk'.format(WHICH_EXP), 'r'))

def Y_gbtree():
    return cPickle.load(open('../out/{0}/Y_gbtree.pk'.format(WHICH_EXP), 'r'))

def svmperf():
    return cPickle.load(open('../out/{0}/svmperf.pk'.format(WHICH_EXP), 'r'))

def dtreeperf():
    return cPickle.load(open('../out/{0}/dtreeperf.pk'.format(WHICH_EXP), 'r'))

def gbtreeperf():
    return cPickle.load(open('../out/{0}/gbtreeperf.pk'.format(WHICH_EXP), 'r'))
