import numpy as np
import pickle
import pandas as pd


which_exp = 'nveMem'
#which_exp = 'nveMemDonA'

Y = pickle.load(open('../out/{0}/Y_proc.pk'.format(which_exp), 'r'))

many_stable = Y['labels'] == 0

how_stable = np.sum(many_stable)/float(len(Y['labels']))

print how_stable
