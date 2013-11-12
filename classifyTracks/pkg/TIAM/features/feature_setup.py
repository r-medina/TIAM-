import numpy as np
import pandas as pd
from glob import glob
import pickle

from TIAM.config import WHICH_EXP
from TIAM.features import FeatureSpace as fs

feature_names = ['straightness',
                 'bending',
                 'efficiency',
                 'asymmetry',
                 'skewness',
                 'kurtosis',
                 'displacement',
                 'confinement']

feat_space = fs.FeatureSpace()
many_features = feat_space.many_features

def feature_setup(labeled=False):
    min_track_len = 20
    labels_dict = {}

    # grabs labels
    if labeled:
        for i, frame in enumerate(glob('../../data/txtData/{0}/labels/*'.format(WHICH_EXP))):
            labels = pd.read_csv(frame, names=['labels'])
            # the keys in the labels_dict dictionary will the index of the
            # cell track in the labels and position data
            if labels.__len__() >= min_track_len:
                labels_dict[i] = labels

    data_dict = {}
    data_head = ['x', 'y', 'footprint']
    # grabs TIAM data
    for j, track in enumerate(glob("../../data/txtData/{0}/data/orig/*".format(WHICH_EXP))):
        raw = pd.read_csv(track, names=data_head)
        if raw.__len__() >= min_track_len:
            data_dict[j] = raw

    # keeps track of the indicies of good tracks
    good_tracks = data_dict.keys()

    assert data_dict.keys(), 'There is no data in specified directory:\n\t../../data/txtData/{0}/data/orig/'.format(WHICH_EXP)

    # loads the data into a pandas panel
    data_panel = pd.Panel(data_dict)

    if labeled:
        assert data_dict.keys() == labels_dict.keys(), 'Data does not correspond to labels'
        # loads the labels into a panel
        labels_panel = pd.Panel(labels_dict)
        return good_tracks, data_panel,feat_space, feature_names, labels_panel

    return good_tracks, data_panel,feat_space, feature_names

