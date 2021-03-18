'''
VisualizationTsneApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData,SQLplateselect,SQLLabel,data_filter,getFlagArr
from ..controller.VisualizationTsneController import getVisualizationTsne

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class Data(Resource):
    '''
    SixDpictureUpDownQuantile
    '''
    def get(self,startTime,endTime):
        """
        get
        ---
        tags:
          - 可视化马雷图部分TSNE
        parameters:
            - in: path
              name: startTime
              required: true
              description: 开始钢板upid
              type: string
            - in: path
              name: endTime
              required: true
              description: 结束钢板upid
              type: string
        responses:
            200:
                description: 执行成功
        """
        tocSelect = [startTime, endTime]
        ismissing = {'dd.all_processes_statistics_ismissing':'0','dd.cool_ismissing':'0','dd.fu_temperature_ismissing':'0','dd.m_ismissing':'0','dd.fqc_ismissing':'0'} 
        data,col_names = SQLLabel(['dd.fqc_label'],ismissing, [], [], [], tocSelect, [], [], 'toc', '')
        data,processdata = data_filter(data,col_names)
        data=data.values
        result = []
        for i in data:
            i[4] = json.dumps(i[4], default=str, ensure_ascii=False)
            flagArr=getFlagArr(i[-1]['method1'])
            label=0
            amount=0
            # for j in flagArr:
            #     amount+=j
            # if(amount>=ref):
            #     label=1
            i[-1] = flagArr[1]
            result.append(dict(zip(col_names, i.tolist())))
        # json.dumps(dict(zip(data.tolist(), col_names.tolist()))

        return result, 200, {'Access-Control-Allow-Origin': '*'}
        # json.dumps(data.tolist())


api.add_resource(Data, '/v1.0/model/data/<startTime>/<endTime>/')