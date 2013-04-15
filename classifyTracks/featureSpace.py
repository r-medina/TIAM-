# Module that generates the panda data frame

import pandas as pd
from glob import glob


def get_dataframe():
    for frame in glob("../data/txtData/nveMemDonA/data/*"):
        #fhandle = open(frame)
        #track_num = frame[:3]
        raw = pd.read_csv(frame, header=None)

    return raw
