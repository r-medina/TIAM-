import pylab as pl
import pandas as pd
import pickle
import os

from get_features import good_tracks, many_features, feature_names


def plothists(X,Y,title,name):
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
    pl.savefig("../out/{0}".format(name),bbox_inches='tight')


if __name__ == "__main__":
    # features
    X = pickle.load(open('../out/X.pk', 'r'))
    # labels
    Y = pickle.load(open('../out/Y.pk', 'r'))
    plothists(X,Y,'Human Labeled','supervised_hist')

    Y = pickle.load(open('../out/Y_hmm.pk', 'r'))
    Y = (Y-1)*-1
    plothists(X,Y,'HMM','hmm_hist')

    Y = pickle.load(open('../out/Y_svm.pk', 'r'))
    plothists(X,Y,'SVM','svm_hist')
