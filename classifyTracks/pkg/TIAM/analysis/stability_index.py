import numpy as np
import pickle
import pandas as pd

def stability_index():
    from TIAM.load_data import Y
    many_stable = Y['labels'] == 0
    how_stable = np.sum(many_stable)/float(len(Y['labels']))
    print how_stable
