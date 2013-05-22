# Module that generates the panda data frame

import pylab as pl
import pandas as pd
from glob import glob
import pickle

import FeatureSpace as fs

labels_dict = {}
i = 0
# grabs labels
for frame in glob("../../data/txtData/nveMemDonA/labels/viv/*"):
    labels = pd.read_csv(frame, names=['labels'])
    labels_dict[i] = labels
    i += 1
# keeps track of how many ar labeled
how_many = i
how_many = 2

data_dict = {}
data_head = ['x', 'y', 'footprint']
i = 0
# grabs TIAM data
while (i <= how_many):
    for track in glob("../../data/txtData/nveMemDonA/data/*"):
        raw = pd.read_csv(track, names=data_head)
        data_dict[i] = raw
        i += 1

# loads the data into a pandas panel
data_panel = pd.Panel(data_dict)

# loads the labels into a panel
labels_panel = pd.Panel(labels_dict)
f_out = open('../out/labels_panel.pk','w')
pickle.dump(labels_panel,f_out)
f_out.close()

feature_names = ['straightness', 'bending', 'efficiency', 'asymmetry',
                 'skewness', 'kurtosis', 'displacement', 'confinement']

feat_space = fs.FeatureSpace()
many_features = feat_space.many_features


def get_dataframe():
    features_dict = {}

    for i in range(how_many):
        pos = pl.array([data_panel[i].dropna(axis=0)['x'], \
                        data_panel[i].dropna(axis=0)['y']])
        pos = pl.transpose(pos)
        features_dict[i] = pd.DataFrame( \
            feat_space.get_features(pos), columns=feature_names)

    features_panel = pd.Panel(features_dict)
    f_out = open('../out/features_panel.pk','w')
    pickle.dump(features_panel,f_out)
    f_out.close()

    # make feat_array and label_arrays so that the following loop can
    # use vstack and hstack
    # we need the arrays to make histograms and such
    feat_array = pl.vstack([features_panel[0].dropna(axis=0)[:], \
                            features_panel[1].dropna(axis=0)[:]])
    label_array = pl.hstack([labels_panel[0].dropna(axis=0)['labels'],\
                             labels_panel[1].dropna(axis=0)['labels']])

    for i in range(2,how_many):
        feat_array = pl.vstack([feat_array, \
                                features_panel[i].dropna(axis=0)[:]])
        label_array = pl.hstack([label_array, \
                                 labels_panel[i].dropna(axis=0)['labels']])
    label_array = pl.transpose(label_array)

    pairs = []
    for track in range(how_many):
        for i in range(len(labels_panel[track].dropna(axis=0).index)):
            pairs.append((track,i))

    multi = pd.MultiIndex.from_tuples(pairs, names=['track', 'frame'])

    print multi
    print feat_array.shape

    X = pd.DataFrame(feat_array,index=multi,columns=feature_names)
    Y = pd.DataFrame(label_array,index=multi,columns=['labels'])

    f_out = open('../out/X.pk','w')
    pickle.dump(X,f_out)
    f_out.close()
    f_out = open('../out/Y.pk','w')
    pickle.dump(Y,f_out)
    f_out.close()

    
if __name__ == "__main__":
    get_dataframe()
