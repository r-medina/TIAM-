# Module that generates the panda data frame

import pylab as pl
import pandas as pd
from glob import glob

import FeatureSpace as fs

def get_dataframe():
    data_dict = {}
    data_head = ['x', 'y', 'footprint']
    i = 0
    # grabs TIAM data
    for track in glob("../data/txtData/nveMemDonA/data/*"):
        raw = pd.read_csv(track, names=data_head)
        data_dict[i] = raw
        i += 1
    howMany = i

    # loads the data into a pandas panel
    data_panel = pd.Panel(data_dict)

    labels_dict = {}
    labels_head = ['labels']
    i = 0
    # grabs labels
    for frame in glob("../data/txtData/nveMemDonA/labels/*"):
        labels = pd.read_csv(frame, names=labels_head)
        labels_dict[i] = labels
        i += 1
    # loads the labels into a panel
    labels_panel = pd.Panel(labels_dict)

    feature_names = ['straightness', 'bending', 'efficiency', 'asymmetry',
                     'skewness', 'kurtosis', 'displacement']

    features_dict = {}

    for i in range(howMany):
        pos = pl.array([data_panel[i].dropna(axis=0)['x'], \
                        data_panel[i].dropna(axis=0)['y']])
        pos = pl.transpose(pos)
        features_dict[i] = pd.DataFrame( \
            fs.FeatureSpace.get_features(pos), columns=feature_names)

    features_panel = pd.Panel(features_dict)
        
    # make feat_array and label_arrays so that the following loop can
    # use vstack and hstack
    # we need the arrays to make histograms and such
    feat_array = pl.vstack([features_panel[0].dropna(axis=0)[:], \
                    features_panel[1].dropna(axis=0)[:]])
    label_array = pl.hstack([labels_panel[0].dropna(axis=0)['labels'],\
                             labels_panel[1].dropna(axis=0)['labels']])

    for i in range(2,howMany):
        feat_array = pl.vstack([feat_array, \
                                features_panel[i].dropna(axis=0)[:]])
        label_array = pl.hstack([label_array, \
                                 labels_panel[i].dropna(axis=0)['labels']])
    label_array = pl.transpose(label_array)

    feats_done = 7
    for i in range(fs.FeatureSpace.many_features):
        a = label_array
        b = feat_array
        pl.figure(i)
        pl.hold()
        if (i==2):
            counts0, bins0 = pl.histogram(b[a==0,i],100,range=(0.,0.08))
            counts1, bins1 = pl.histogram(b[a==1,i],100,range=(0.,0.08))
        elif (i==5):
            counts0, bins0 = pl.histogram(b[a==0,i],100,range=(1,5))
            counts1, bins1 = pl.histogram(b[a==1,i],100,range=(1,5))
        elif (i==6):
            counts0, bins0 = pl.histogram(b[a==0,i],100,range=(0,15))
            counts1, bins1 = pl.histogram(b[a==1,i],100,range=(0,15))
        else:
            counts0, bins0 = pl.histogram(b[a==0,i],100)
            counts1, bins1 = pl.histogram(b[a==1,i],100)
        pl.plot(bins0[0:100],counts0,'r',bins1[0:100],counts1,'b')
        pl.title(feature_names[i])
    pl.show()


if __name__ == "__main__":
    get_dataframe()
