import os, sys

abspath = lambda *p: os.path.abspath(os.path.join(*p))
PROJECT_ROOT = abspath(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#from TIAM import features, anaylsis

#features.get_features()
#analysis.analysis()
