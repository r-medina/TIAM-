import numpy as np
import pandas as pd
from glob import glob
import cPickle

from TIAM.config import WHICH_EXP
from TIAM import mkdir
from TIAM.features.feature_setup import feature_setup


def get_features(labeled=False):
    mkdir.mkdir('../out/{0}'.format(WHICH_EXP))

    if labeled:
        good_tracks, data_panel,feat_space, feature_names, labels_panel = feature_setup(labeled)
    else:
        good_tracks, data_panel,feat_space, feature_names = feature_setup(labeled)

    features_dict = {}
    for i in good_tracks:
        pos = np.array([data_panel[i].dropna(axis=0)['x'],
                        data_panel[i].dropna(axis=0)['y']])
        pos = np.transpose(pos)
        features_dict[i] = pd.DataFrame(feat_space.get_features(pos),
                                        columns=feature_names)

    features_panel = pd.Panel(features_dict)

    # make feat_array and label_arrays so that the following loop can
    # use vstack and hstack
    # we need the arrays to make histograms and such
    feat_array = np.vstack([features_panel[good_tracks[0]].dropna(axis=0)[:],
                            features_panel[good_tracks[1]].dropna(axis=0)[:]])
    if labeled:
	label_array = np.hstack([labels_panel[good_tracks[0]].dropna(axis=0)['labels'],
				 labels_panel[good_tracks[1]].dropna(axis=0)['labels']])
    
    for i in good_tracks[2:]:
        feat_array = np.vstack([feat_array,
                                features_panel[i].dropna(axis=0)[:]])
	if labeled:
	    label_array = np.hstack([label_array,
				     labels_panel[i].dropna(axis=0)['labels']])
    if labeled:
	label_array = np.transpose(label_array)

    pairs = []
    for track in good_tracks:
	for i in range(len(data_panel[track].dropna(axis=0).index)):
            pairs.append((track,i))

    multi = pd.MultiIndex.from_tuples(pairs, names=['track', 'frame'])

    X = pd.DataFrame(feat_array,index=multi,columns=feature_names)
    cPickle.dump(X,open('../out/{0}/X.pk'.format(WHICH_EXP),'w'))

    if labeled:
	Y = pd.DataFrame(label_array,index=multi,columns=['labels'])
	cPickle.dump(Y,open('../out/{0}/Y_supervised.pk'.format(WHICH_EXP),'w'))
