import pylab as pl
import pandas as pd

from TIAM.config import WHICH_EXP
from TIAM.analysis import load_data
#from TIAM.features.feature_setup import good_tracks, many_features, feature_names
from TIAM.features.feature_setup import feature_names, many_features, feature_setup

def plot_hist(X,Y,title,name):
    # get list of tracks and list of labels
    xs = X.values
    ys = Y.values
    ys = pl.reshape(ys,[ys.shape[0],])
    
    pl.figure(figsize=(15, 6), dpi=100)
    for i in range(many_features):
        if (i==2):
            counts0, bins0 = pl.histogram(xs[ys==0,i],100,range=(0.,0.08))
            counts1, bins1 = pl.histogram(xs[ys==1,i],100,range=(0.,0.08))
        elif (i==5):
            counts0, bins0 = pl.histogram(xs[ys==0,i],100,range=(1,5))
            counts1, bins1 = pl.histogram(xs[ys==1,i],100,range=(1,5))
        elif (i==6):
            counts0, bins0 = pl.histogram(xs[ys==0,i],100,range=(0,15))
            counts1, bins1 = pl.histogram(xs[ys==1,i],100,range=(0,15))
        elif (i==7):
            counts0, bins0 = pl.histogram(xs[ys==0,i],100,range=(-1.5,1.))
            counts1, bins1 = pl.histogram(xs[ys==1,i],100,range=(-1.5,1.))	      
        else:
            counts0, bins0 = pl.histogram(xs[ys==0,i],100)
            counts1, bins1 = pl.histogram(xs[ys==1,i],100)
        pl.hold()
        pl.subplot(2,4,i+1)
        pl.plot(bins0[0:100],counts0,'r',bins1[0:100],counts1,'b')
        pl.title(feature_names[i])
    pl.tight_layout()
    pl.savefig("../out/{0}/{1}".format(WHICH_EXP,name),bbox_inches='tight')


def plot(labeled=False):
    X = load_data.X()

    if labeled:
        Y_supervised = load_data.Y_supervised()
        good_tracks, data_panel,feat_space, feature_names, labels_panel = feature_setup(labeled)
        plot_hist(X,Y_supervised,'Human Labeled','supervised_hist')
    else:
        good_tracks, data_panel,feat_space, feature_names = feature_setup(labeled)
    
    Y_hmm = load_data.Y_hmm()
    plot_hist(X,Y_hmm,'HMM','hmm_hist')

    Y_svm = load_data.Y_svm()
    plot_hist(X,Y_svm,'SVM','svm_hist')
