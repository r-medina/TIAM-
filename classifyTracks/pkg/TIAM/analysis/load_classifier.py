import pickle
from TIAM.config import WHICH_EXP
    
def hmmc():
    return pickle.load(open('../out/{0}/hmmc.pk'.format(WHICH_EXP), 'r'))

def svmc():
    return pickle.load(open('../out/{0}/svmc.pk'.format(WHICH_EXP), 'r'))

def dtreec():
    return pickle.load(open('../out/{0}/dtreec.pk'.format(WHICH_EXP), 'r'))

def gbtreec():
    return pickle.load(open('../out/{0}/gbtreec.pk'.format(WHICH_EXP), 'r'))
