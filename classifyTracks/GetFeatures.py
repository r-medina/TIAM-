# Module that generates the panda data frame

import pylab as pl
import pandas as pd
from glob import glob

import FeatureSpace as fs

def get_dataframe():
    data_dict = {}
    i = 0
    for frame in glob("../data/txtData/nveMemDonA/data/*"):
        data_head = ['x', 'y', 'footprint']
        #raw = pd.read_csv(frame, header=None)
        raw = pd.read_csv(frame, names=data_head)
        data_dict[i] = raw
        i += 1
    howMany = i
    howMany = 38#38

    data_panel = pd.Panel(data_dict)

    labels_dict = {}
    i = 0
    for frame in glob("../data/txtData/nveMemDonA/labels/*"):
        labels_head = ['labels']
        #raw = pd.read_csv(frame, header=None)
        labels = pd.read_csv(frame, names=labels_head)
        labels_dict[i] = labels
        i += 1
    labels_panel = pd.Panel(labels_dict)

    features_dict = {}

    for i in range(howMany):
        pos = pl.array([data_panel[i].dropna(axis=0)['x'], \
                        data_panel[i].dropna(axis=0)['y']])
        pos = pl.transpose(pos)
        features_dict[i] = fs.FeatureSpace.get_features(pos)

    #features_panel = pd.Panel(features_dict)
    features_panel = features_dict
    feats_done = 6
        
    feat_array = pl.vstack([features_panel[0][:,0:feats_done], \
                            features_panel[1][:,0:feats_done]])
    label_array = pl.hstack([labels_panel[0].dropna(axis=0)['labels'],\
                             labels_panel[1].dropna(axis=0)['labels']])

    for i in range(2,howMany):
        feat_array = pl.vstack([feat_array,features_panel[i][:,0:feats_done]])
        label_array = pl.hstack([label_array,\
                                 labels_panel[i].dropna(axis=0)['labels']])
    label_array = pl.transpose(label_array)

    for i in range(feats_done):
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
        else:
            counts0, bins0 = pl.histogram(b[a==0,i],100)
            counts1, bins1 = pl.histogram(b[a==1,i],100)
        pl.plot(bins0[0:100],counts0,'r',bins1[0:100],counts1,'b')
    pl.show()


get_dataframe()
