'''
VisualizationTsneController
'''

import math
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from itertools import groupby
from scipy import interpolate
from dateutil.parser import parse
import os
import pandas as pd
import json
import datetime
from sklearn.manifold import TSNE
from ..utils import getFlagArr
from ..utils import ref


class getVisualizationTsne:
    '''
    getVisualizationTsne
    '''

    def __init__(self):
        print('生成实例')

    def run(self, data,processdata):

        X_embedded = TSNE(n_components=2).fit_transform(processdata)
        index=0
        upload_json={}
        data=np.array(data)
        for i in data:
            time = json.dumps(i[4], default=str, ensure_ascii=False)
            time = json.loads(time)
            flagArr=getFlagArr(i[-1]['method1'])
            label=0
            amount=0
            for j in flagArr:
                amount+=j
            if(amount>=ref):
                label=1
            upload_json[str(index)]={
                "x":X_embedded[index][0].item(),
                "y":X_embedded[index][1].item(),
                "toc":time,
                "upid":i[1],
                "productcategory":i[2],
                "tgtplatelength2":i[7],
                "tgtplatethickness2":i[5],
                "tgtwidth":i[6],
                "ave_temp_dis":i[-2]['data'][10],					
                "crowntotal":i[-2]['data'][76],
                "wedgetotal":i[-2]['data'][88],
                "finishtemptotal":i[-2]['data'][96],
                "avg_p5":i[-2]['data'][100],
                'label':str(label)
            }
            index+=1
        return  upload_json




