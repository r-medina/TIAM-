import numpy as np
import cPickle
import pandas as pd
from TIAM.analysis import classify
from TIAM.config import WHICH_EXP
from TIAM.analysis import load_data

epsilon = 0.0000000000000001

def accuracy(y_sup,y_pred):
    return float(1 - (np.abs(y_sup - y_pred).sum() / y_sup.shape[0]))

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
    sens = tp/(tp+float(fn)+epsilon)
    spec = tn/(tn+float(fp)+epsilon)
    return conf_matrix, sens, spec
    
def test_results():
    Y = load_data.Y_proc()
    Y_hmm = load_data.Y_hmm()
    Y_svm = load_data.Y_svm()
    svmperf = load_data.svmperf()
    Y_dtree = load_data.Y_dtree()
    dtreeperf = load_data.dtreeperf()
    Y_gbtree = load_data.Y_gbtree()
    gbtreeperf = load_data.gbtreeperf()
    
    hmm_acc = accuracy(Y,Y_hmm)
    if (hmm_acc < 0.5):
        Y_hmm = (Y_hmm - 1)*-1
        cPickle.dump(Y_hmm, open('../out/{0}/Y_hmm.pk'.format(WHICH_EXP), 'w'))
        hmm_acc = accuracy(Y,Y_hmm)
    
    svm_acc = accuracy(Y,Y_svm)
    dtree_acc = accuracy(Y,Y_dtree)
    gbtree_acc = accuracy(Y,Y_gbtree)

    hmm_conf, hmm_sens, hmm_spec = test(Y,Y_hmm)
    svm_conf, svm_sens, svm_spec = test(Y,Y_svm)
    dtree_conf, dtree_sens, dtree_spec = test(Y,Y_dtree)
    gbtree_conf, gbtree_sens, gbtree_spec = test(Y,Y_gbtree)
    
    def print_results(which,acc,conf,sens,spec,perf=[]):
        try:
            res = '{}\n\taccuracy:\t{:.4}\n\tmean, stdev:\t{:.4}, {:.4} (under 10-fold CV)\n\tsensitivity:\t{:.4}\n\tspecificity:\t{:.4}\n'.format(which,acc,perf.mean(),perf.std(),sens,spec)
        except:
            res = '{}\n\taccuracy:\t{:.4}\n\tsensitivity:\t{:.4}\n\tspecificity:\t{:.4}\n'.format(which,acc,sens,spec)

        with open('../out/{0}/performance.txt','w') as fo:
            f.write(res)
        # print which
        # print '\taccuracy:\t{0:.4}'.format(acc)
        # try:
        #     print '\tmean, stdev:\t{0:.4}, {1:.4} (under 10-fold CV)'.format(perf.mean(),perf.std())
        # except:
        #     pass
        # print "\tsensitivity:\t{0:.4}".format(sens)
        # print "\tspecificity:\t{0:.4}\n".format(spec)
    
    print_results('HMM',hmm_acc,hmm_conf,hmm_sens,hmm_spec)
    print_results('SVM',svm_acc,svm_conf,svm_sens,svm_spec,svmperf)
    print_results('DTree',dtree_acc,dtree_conf,dtree_sens,dtree_spec,dtreeperf)
    # this is wildly overfit. don't know how to use best
    # cross-validated classifier instead
    print_results('GBTree',gbtree_acc,gbtree_conf,gbtree_sens,gbtree_spec,gbtreeperf)
