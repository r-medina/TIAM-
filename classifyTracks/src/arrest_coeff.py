import numpy as np
import pandas as pd
import pickle

import FeatureSpace as fs

which_exp = 'nveMem'
Y = pickle.load(open('../out/{0}/Y.pk'.format(which_exp), 'r'))

def classify_by_arrest_coeff(dist,threshold):
    return [int(np.linalg.norm(x)>threshold) for x in dist]

feat_space = fs.FeatureSpace()

from get_features import data_panel, good_tracks


def test_arrest(threshold):
    predict_dict = {}

    i = 0
    for track in good_tracks:
	pos = np.array([data_panel[track].dropna(axis=0)['x'], \
			data_panel[track].dropna(axis=0)['y']])
	pos = np.transpose(pos)
	track_length = pos.shape[0]
    
	steps = feat_space.get_steps(pos,len(pos))
	disp = np.zeros(track_length-1)

	predict_dict[i] = classify_by_arrest_coeff(steps,threshold)
	i+=1

    predict_array = np.array([666])
    for track in predict_dict.items():
	for prediction in track:
	    predict_array = np.hstack([predict_array,prediction])

    predict_array = predict_array[1:]
    print predict_array == Y['labels'].__array__()
    perf =  np.sum([int(x) for x in (predict_array == Y['labels'].__array__())])/float(len(predict_array))
    
    return perf

results = np.array([test_arrest(x) for x in np.linspace(0,2,100)])
print np.max(results)
