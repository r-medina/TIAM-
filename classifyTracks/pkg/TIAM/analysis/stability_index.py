import numpy as np
import pickle
import pandas as pd

from TIAM.analysis import load_data


def stability_index(labeled=False):
    if labeled:
	Y = load_data.Y_supervised()
    else:
	Y = load_Data.Y_predicted()
    many_stable = Y['labels'] == 0
    how_stable = np.sum(many_stable)/float(len(Y['labels']))
    print how_stable
