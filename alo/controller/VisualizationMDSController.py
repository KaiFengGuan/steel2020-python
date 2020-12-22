'''
VisualizationMDSController
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
from sklearn.manifold import MDS
from ..utils import getFlagArr
from ..utils import ref



class getVisualizationMDS:
    '''
    getVisualizationMDS
    '''

    def __init__(self):
        print('生成实例')

    def run(self,data):
        # read data from database which has character:
        # toc，upid，productcategory，tgtplatelength2，tgtplatethickness2，tgtwidth，ave_temp_dis，
        # crowntotal，nmrPre_params，wedgetotal，finishtemptotal，avg_p5

        # N=1000 #样本数

        # M=300 #一维变量维度

        # X = np.random.random((N,M))
        # X = np.random.random((2,3))
        # print(X)
        # embedding = MDS(n_components=2)

        # X_transformed = embedding.fit_transform(X)
        # toc，upid，productcategory，tgtplatelength2，tgtplatethickness2，tgtwidth，ave_temp_dis，crowntotal，nmrPre_params，wedgetotal，finishtemptotal，avg_p5

        N=len(data)
        M=data[0][6]['data']
        X=[]
        # embedding = MDS(n_components=2)
        for i in data:
            X.append(i[6]['data'])
            # print(len(i[6]['data']))
        # print(X)
        # print(len(X))
        embedding = MDS(n_components=2)

        X_transformed = embedding.fit_transform(X)
        # print(X_transformed)

        toc=[]
        upid=[]
        productcategory=[]
        tgtplatelength2=[]
        tgtplatethickness2=[]
        tgtwidth=[]
        ave_temp_dis=[]
        crowntotal=[]
        nmrPre_params=[]
        wedgetotal=[]
        finishtemptotal=[]
        avg_p5=[]
        X=[]
        Y=[]
        index=0
        upload_json={}
        # while (index<len(data)):
        #     time=data[i][2]
        #     time = json.dumps(time, default=str, ensure_ascii=False)
            
        #     # 把data再次转为json类型即可
        #     time = json.loads(time)
        #     upload_json[str(i)]={"x":X[i][0],"y":Y[i][1],"toc":time,"upid":data[i][0],"productcategory":data[i][1],"tgtplatelength2":data[i][4],
		#     "tgtplatethickness2":data[i][5],"tgtwidth":data[i][3],"ave_temp_dis":data[6]['data'][10],					
		#     "crowntotal":data[6]['data'][76],"wedgetotal":data[6]['data'][88],"finishtemptotal":data[6]['data'][96],"avg_p5":data[6]['data'][100]}
        for i in data:
            time = json.dumps(i[2], default=str, ensure_ascii=False)
            
            # 把data再次转为json类型即可
            time = json.loads(time)
            flagArr=getFlagArr(i[7]['method1'])
            label=0
            amount=0
            for j in flagArr:
                amount+=j
            if(amount>=ref):
                label=1
            upload_json[str(index)]={"x":X_transformed[index][0],"y":X_transformed[index][1],"toc":time,"upid":i[0],"productcategory":i[1],"tgtplatelength2":i[4],
		    "tgtplatethickness2":i[5],"tgtwidth":i[3],"ave_temp_dis":i[6]['data'][10],					
		    "crowntotal":i[6]['data'][76],"wedgetotal":i[6]['data'][88],"finishtemptotal":i[6]['data'][96],"avg_p5":i[6]['data'][100],'label':str(label)}
            index+=1
        #     upid.append(i[0])
        #     productcategory.append(i[1])
            
        #     time = json.dumps(i[2], default=str, ensure_ascii=False)
            
        #     # 把data再次转为json类型即可
        #     time = json.loads(time)
        #     toc.append(time)
        #     tgtwidth.append(i[3])
        #     tgtplatelength2.append(i[4])
        #     tgtplatethickness2.append(i[5])
        #     ave_temp_dis.append(i[6]['data'][10])
        #     crowntotal.append(i[6]['data'][76])
        #     wedgetotal.append(i[6]['data'][88])
        #     finishtemptotal.append(i[6]['data'][96])
        #     avg_p5.append(i[6]['data'][100])
        # for i in X_transformed:
        #     X.append(i[0])
        #     Y.append(i[1])
        

        # X_transformed = embedding.fit_transform(M)
        # print(X_transformed)
        # path1 = os.path.abspath('.')+'/alo/MDS_data.data'

        # # fp = open(r"./MDS_data")
        # fp = open(path1)

        # allMDS = fp.readlines()
        # fp.close()

        # allMDS_df = pd.DataFrame(json.loads(allMDS[0])).T

        # allMDS_df['toc'] = pd.to_datetime(allMDS_df['toc'])

        # startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        # endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")

        # somePlate_df_tmp = allMDS_df[allMDS_df['toc'] >= startTime]
        # somePlate_df = somePlate_df_tmp[somePlate_df_tmp['toc'] <= endTime]

        # somePlate_json = somePlate_df.T.to_json(orient='columns', force_ascii=False)
        # somePlate_json = json.loads(somePlate_json)

        return  upload_json




