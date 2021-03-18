'''
VisualizationPCAController
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
import umap

from ..utils import getFlagArr
from ..utils import ref
# umap-learn
# umap-learn[plot]
# umap-learn[plot]
# umap-learn
class getVisualizationPCA:
    '''
    getVisualizationPCA
    '''

    def __init__(self):
        print('生成实例')

    def run(self,data,process_data,col_names):
        print(process_data.shape)  
        norm_process_data = (process_data - process_data.min()) / (process_data.max() - process_data.min())
        X_transformed = umap.UMAP().fit(norm_process_data).embedding_.astype('float64')
        print(X_transformed.shape)      
        print(type(X_transformed)) 
        index=0
        upload_json={}
        data=data.values
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
        return upload_json




