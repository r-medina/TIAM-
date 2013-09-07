import numpy as np
import pandas as pd
from glob import glob
import pickle

from TIAM import mkdir
from TIAM.config import WHICH_EXP
from TIAM.features import FeatureSpace as fs

min_track_len = 20
labels_dict = {}
i = 0
mkdir.mkdir('../out/{0}'.format(WHICH_EXP))


# grabs labels
for frame in glob('../../data/txtData/{0}/labels/*'.format(WHICH_EXP)):
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
for track in glob("../../data/txtData/{0}/data/orig/*".format(WHICH_EXP)):
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