'''
VisualizationMDSController
'''

import math
import requests
import numpy as np
import seaborn as sns

from itertools import groupby
from scipy import interpolate
from dateutil.parser import parse
import os
import pandas as pd
import json
import datetime
from sklearn.manifold import Isomap
from ..utils import getFlagArr,ref



class getVisualizationMDS:
    '''
    getVisualizationMDS
    '''

    def __init__(self):
        print('生成实例')

    def run(self,data,process_data,col_names):
        
        norm_process_data = (process_data - process_data.min()) / (process_data.max() - process_data.min())
        X_transformed = Isomap (n_components=2).fit_transform(norm_process_data)

        index=0
        upload_json={}
        data= np.array(data)
        for i in data:
            flagArr=getFlagArr(i[-1]['method1'])
            label=flagArr[1]
            singlesteel = dict(zip(col_names, i.tolist()))
            singlesteel["toc"] = json.loads(json.dumps(i[4], default=str, ensure_ascii=False))
            singlesteel["x"] = X_transformed[index][0]
            singlesteel["y"] = X_transformed[index][1]
            singlesteel["label"] = str(label)
            
            upload_json[str(index)]=singlesteel
            index+=1

        return  upload_json




