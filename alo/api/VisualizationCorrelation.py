'''
Visualization
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
import numpy as np
from ..utils import getData,SQLLabel,data_filter
from ..utils import getFlagArr
import json
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from scipy.interpolate import interp1d
from scipy.stats import pearsonr
from sklearn import metrics

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class VisualizationCorrelation(Resource):
    '''
    SixDpictureUpDownQuantile
    '''
    def get(self,startTime,endTime):
        """
        get
        ---
        tags:
          - 可视化相关性分析
        parameters:
            - in: path
              name: startTime
              required: true
              description: 开始时间
              type: string
            - in: path
              name: endTime
              required: true
              description: 结束时间
              type: string
        responses:
            200:
                description: 执行成功
        """
        # ismissing={'all_processes_statistics_ismissing':True}
        # selection=['all_processes_statistics','all_processes_statistics_ismissing','cool_ismissing','fu_temperature_ismissing','m_ismissing','fqc_ismissing']
        # data = getData(['all_processes_statistics','all_processes_statistics_ismissing','cool_ismissing','fu_temperature_ismissing','m_ismissing','fqc_ismissing'], ismissing, [], [], [], [startTime,endTime], [], [], '', '')
        ismissing = {'dd.all_processes_statistics_ismissing':'0','dd.cool_ismissing':'0','dd.fu_temperature_ismissing':'0','dd.m_ismissing':'0','dd.fqc_ismissing':'0'}
        data,col_names = SQLLabel(['dd.all_processes_statistics_ismissing','dd.cool_ismissing','dd.fu_temperature_ismissing','dd.m_ismissing','dd.fqc_ismissing'],ismissing, [], [], [], [startTime,endTime], [], [], '', '')
        data,processdata=data_filter(data,col_names)
        
        processdata= data[col_names[5:134]].values
        # np.array(data)
        data=np.array(data)
        fault=data[:,134:139]
        print('fhuedui')
        print(processdata.shape)
        print(fault.shape)
        col_names = col_names[5:134]

        jsondata={'data':[]}
        sortData = {}

        processdata=processdata.T
        fault=np.array(fault)
        # print(fault.shape)
        fault=fault.swapaxes(0,1)
        nmi_matrix = np.zeros([len(processdata),len(fault)]) #初始化互信息矩阵
        for i in range(len(processdata)):
            for j in range(len(fault)):
                nmi_matrix[i][j] = metrics.normalized_mutual_info_score(processdata[i], fault[j])
        result=np.abs(nmi_matrix.swapaxes(0,1)).tolist()
        faultSum = np.zeros(len(processdata))
        for i in range(len(result)):
            jsondata['data'].append({'fault'+repr(i):result[i]})
            faultSum = np.array(result[i]) + faultSum
            sortData['fault'+repr(i)] = result[i]
            # print(len(result[i]))
        jsondata['label']=col_names
        # print(len(columnslabel))

        dataIndex = np.array(range(len(processdata)))

        sortDataFrame = {'faultSum': faultSum, 'dataIndex': dataIndex}
        sortDataFrame = pd.DataFrame(sortDataFrame)
        sortDataFrame = sortDataFrame.sort_values(by="faultSum",ascending=True)
        indexArr = sortDataFrame['dataIndex'].values

        sortData['label'] = col_names
        sortData = pd.DataFrame(sortData)

        sortData = sortData.loc[indexArr]
        sortData = sortData.to_dict('list')
        print(processdata.shape)
        print(type(processdata))
        corrdata=np.corrcoef(processdata.astype(np.float32))
        print(corrdata.shape)
        print(np.isfinite(processdata).sum())
        print(np.isinf(processdata).sum())
        X_embedded = TSNE(n_components=2).fit_transform(processdata)
        # print(X_embedded)
        # print(X_embedded.shape)

        sortData['corr']=corrdata.tolist()
        sortData['position']=X_embedded.tolist()
        return sortData, 200, {'Access-Control-Allow-Origin': '*'}
        return processdata.tolist()
api.add_resource(VisualizationCorrelation, '/v1.0/model/VisualizationCorrelation/<startTime>/<endTime>/')