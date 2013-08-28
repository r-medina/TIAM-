import numpy as np
import pickle
import pandas as pd

from tiam.load_data import Y


many_stable = Y['labels'] == 0

how_stable = np.sum(many_stable)/float(len(Y['labels']))

print how_stable
