import numpy as np
import pickle
import pandas as pd


which_exp = 'nveMem'
#which_exp = 'nveMemDonA'

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
    

Y = pickle.load(open('../out/{0}/Y_proc.pk'.format(which_exp), 'r'))
Y_hmm = pickle.load(open('../out/{0}/Y_hmm.pk'.format(which_exp), 'r'))
Y_svm = pickle.load(open('../out/{0}/Y_svm.pk'.format(which_exp), 'r'))

hmm_acc = accuracy(Y,Y_hmm)
if (hmm_acc < 0.5):
    Y_hmm = (Y_hmm - 1)*-1
    hmm_acc = accuracy(Y,Y_hmm)

svm_acc = accuracy(Y,Y_svm)

hmm_conf, hmm_sens, hmm_spec = test(Y,Y_hmm)
svm_conf, svm_sens, svm_spec = test(Y,Y_svm)

def print_results(which,acc,conf,sens,spec):
    print which
    print "\taccuracy:\t{0:.4}".format(acc['labels'])
    print "\tsensitivity:\t{0:.4}".format(sens)
    print "\tspecificity:\t{0:.4}\n".format(spec)

print_results('SVM',svm_acc,svm_conf,svm_sens,svm_spec)
print_results('HMM',hmm_acc,hmm_conf,hmm_sens,hmm_spec)
