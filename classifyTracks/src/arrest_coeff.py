import numpy as np
import pandas as pd
import pickle

import FeatureSpace as fs

threshold = 3.

def classify_by_arrest_coeff(dist):
    predictions = [int(x>threshold) for x in dist]
    return predictions

feat_space = fs.FeatureSpace()

from get_features import data_panel, good_tracks

predict_dict = {}

i = 0
for track in good_tracks:
    pos = np.array([data_panel[track].dropna(axis=0)['x'], \
                    data_panel[track].dropna(axis=0)['y']])
    pos = np.transpose(pos)
    track_length = pos.shape[0]
    
    steps = feat_space.get_steps(pos)
    disp = np.zeros(track_length-1)

    #predict_dict[i] = classify_by_arrest_coeff(steps)
    i+=1
