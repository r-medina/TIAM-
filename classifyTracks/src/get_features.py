# Module that generates the pandas data frame

import pylab as pl
import pandas as pd
from glob import glob
import pickle

import FeatureSpace as fs


which_exp = 'nveMem'

min_track_len = 20
labels_dict = {}
i = 0
# grabs labels
#for frame in glob('../../data/txtData/nveMemDonA/labels/viv/*'):
for frame in glob('../../data/txtData/{0}/labels/*'.format(which_exp)):
    labels = pd.read_csv(frame, names=['labels'])
    # the keys in the labels_dict dictionary will the index of the
    # cell track in the labels and position data
    if labels.__len__() >= min_track_len:
        labels_dict[i] = labels
    i += 1
# keeps track of the indicies of the 
good_tracks = labels_dict.keys()

data_dict = {}
data_head = ['x', 'y', 'footprint']
i = 0
# grabs TIAM data
#for track in glob("../../data/txtData/nveMemDonA/data/attached/*"):
for track in glob("../../data/txtData/{0}/data/orig/*".format(which_exp)):
    raw = pd.read_csv(track, names=data_head)
    if raw.__len__() >= min_track_len:
        data_dict[i] = raw
    i += 1

# loads the data into a pandas panel
data_panel = pd.Panel(data_dict)

# loads the labels into a panel
labels_panel = pd.Panel(labels_dict)

feature_names = ['straightness', 'bending', 'efficiency', 'asymmetry',
                 'skewness', 'kurtosis', 'displacement', 'confinement']

feat_space = fs.FeatureSpace()
many_features = feat_space.many_features


def get_features():
    features_dict = {}
    for i in good_tracks:
        pos = pl.array([data_panel[i].dropna(axis=0)['x'], \
                        data_panel[i].dropna(axis=0)['y']])
        pos = pl.transpose(pos)
        features_dict[i] = pd.DataFrame( \
            feat_space.get_features(pos), columns=feature_names)

    features_panel = pd.Panel(features_dict)

    # make feat_array and label_arrays so that the following loop can
    # use vstack and hstack
    # we need the arrays to make histograms and such
    feat_array = pl.vstack([features_panel[good_tracks[0]].dropna(axis=0)[:], \
                            features_panel[good_tracks[1]].dropna(axis=0)[:]])
    label_array = pl.hstack([labels_panel[good_tracks[0]].dropna(axis=0)['labels'],\
                             labels_panel[good_tracks[1]].dropna(axis=0)['labels']])
    
    for i in good_tracks[2:]:
        feat_array = pl.vstack([feat_array, \
                                features_panel[i].dropna(axis=0)[:]])
        label_array = pl.hstack([label_array, \
                                 labels_panel[i].dropna(axis=0)['labels']])
    label_array = pl.transpose(label_array)

    pairs = []
    for track in good_tracks:
        for i in range(len(labels_panel[track].dropna(axis=0).index)):
            pairs.append((track,i))

    multi = pd.MultiIndex.from_tuples(pairs, names=['track', 'frame'])

    X = pd.DataFrame(feat_array,index=multi,columns=feature_names)
    Y = pd.DataFrame(label_array,index=multi,columns=['labels'])


    pickle.dump(X,open('../out/{0}/X.pk'.format(which_exp),'w'))
    pickle.dump(Y,open('../out/{0}/Y.pk'.format(which_exp),'w'))

    
if __name__ == "__main__":
    get_features()
