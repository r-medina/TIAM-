import numpy as np
import pickle
import pandas as pd

def accuracy(y_sup,y_pred):
    return 1 - (np.abs(y_sup - y_pred).sum() / y_sup.shape[0])

def test(y_sup,y_pred):
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    y_sup = y_sup.values
    y_pred = y_pred.values
    for i in range(len(y_pred)):
        if y_pred[i] == 1:
            if y_sup[i] == 1:
                tp += 1
            else:
                fn += 1
        else:
            if y_sup[i] == 1:
                fp += 1
            else:
                tn +=1
    conf_matrix = np.array([[tp,fn],[fp,tn]])
    sens = tp/(tp+float(fn))
    spec = tn/(tn+float(fp))
    return conf_matrix, sens, spec
    

Y = pickle.load(open('../out/Y.pk', 'r'))
Y_hmm = pickle.load(open('../out/Y_hmm.pk', 'r'))
Y_hmm = (Y_hmm - 1)*-1
Y_svm = pickle.load(open('../out/Y_svm.pk', 'r'))

hmm_acc = accuracy(Y,Y_hmm)
svm_acc = accuracy(Y,Y_svm)

hmm_conf, hmm_sens, hmm_spec = test(Y,Y_hmm)
svm_conf, svm_sens, svm_spec = test(Y,Y_svm)
