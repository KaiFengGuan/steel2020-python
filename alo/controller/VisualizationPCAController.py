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

from sklearn.decomposition import PCA
from ..utils import getFlagArr
from ..utils import ref


class getVisualizationPCA:
    '''
    getVisualizationPCA
    '''

    def __init__(self):
        print('生成实例')

    def run(self,data):
# used to fix remote data
        # read data from database which has character:
        # toc，upid，productcategory，tgtplatelength2，tgtplatethickness2，
        # tgtwidth，ave_temp_dis，crowntotal，nmrPre_params，wedgetotal，finishtemptotal，avg_p5
        # N=1000 #样本数

        # M=300 #一维变量维度

        # X = np.random.random((N,M))

        # pca = PCA(n_components=2)

        # pca.fit(X)

        # X_transformed = pca.transform(X)
        # print(X_transformed)
        # selectSql = "select * from dcenter.dump_data where upid='" + '18901034000' + "'"
        # selectSql = "select upid, toc, fqc_label from dcenter.dump_data where fqc_ismissing = 0 and toc>='2018-09-01 00:00:00' and toc<='2018-09-02 00:00:00' "
        # data = getDataBySql(selectSql)


        # path1 = os.path.abspath('.')+'/alo/PCA_data.data'

        # # fp = open(r"./PCA_data")
        # fp = open(path1)

        # allPCA = fp.readlines()
        # fp.close()

        # allPCA_df = pd.DataFrame(json.loads(allPCA[0])).T

        # allPCA_df['toc'] = pd.to_datetime(allPCA_df['toc'])

        # startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        # endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")

        # somePlate_df_tmp = allPCA_df[allPCA_df['toc'] >= startTime]
        # somePlate_df = somePlate_df_tmp[somePlate_df_tmp['toc'] <= endTime]

        # somePlate_json = somePlate_df.T.to_json(orient='columns', force_ascii=False)
        # somePlate_json = json.loads(somePlate_json)

        # return somePlate_json
        # print(data)


        N=len(data)
        M=data[0][6]['data']
        X=[]
        # embedding = MDS(n_components=2)
        for i in data:
            X.append(i[6]['data'])
            # print(len(i[6]['data']))
        pca = PCA(n_components=2)

        pca.fit(X)

        X_transformed = pca.transform(X)

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
        for i in data:
            time = json.dumps(i[2], default=str, ensure_ascii=False)
            
            # 把data再次转为json类型即可
            time = json.loads(time)
            flagArr=getFlagArr(i[7]['method1'])
            label=0
            amount=0
            for j in flagArr:
                amount+=j
            if(amount >= ref):
                label=1
            upload_json[str(index)]={"x":X_transformed[index][0],"y":X_transformed[index][1],"toc":time,"upid":i[0],"productcategory":i[1],"tgtplatelength2":i[4],
		    "tgtplatethickness2":i[5],"tgtwidth":i[3],"ave_temp_dis":i[6]['data'][10],					
		    "crowntotal":i[6]['data'][76],"wedgetotal":i[6]['data'][88],"finishtemptotal":i[6]['data'][96],"avg_p5":i[6]['data'][100],'label':str(label)}
            index+=1
        return upload_json



