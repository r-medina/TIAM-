import pickle
from TIAM.config import *

# Loads the data to be used by the other parts of the package after
# the features have been generated
X = pickle.load(open('../out/{0}/X.pk'.format(WHICH_EXP), 'r'))
Y = pickle.load(open('../out/{0}/Y.pk'.format(WHICH_EXP), 'r'))
