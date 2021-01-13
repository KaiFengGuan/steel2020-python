'''
VisualizationMDSApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData
from ..utils import getFlagArr
from ..utils import ref

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class getFlag(Resource):
    '''
    getFlag
    '''
    def get(self,startTime,endTime):
        """
        get
        ---
        tags:
          - 获取钢板标签
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
        # return {'hello': 'world'}
        tocSelect = [startTime, endTime]
        ismissing = {'all_processes_statistics_ismissing':True,'cool_ismissing':True,'fu_temperature_ismissing':True,'m_ismissing':True,'fqc_ismissing':True} 
        data = getData(['upid', 'fqc_label'], {}, [], [], [], tocSelect, [], [], '', '')
        
        result = {}
        # print(data)
        for item in data:
            label=0
            amount=0
            if 'method1' in item[1]:
                flagArr=getFlagArr(item[1]['method1'])
                # for j in flagArr:
                #     amount+=j
                # if(amount>=ref):
                #     label=1
                # print(flagArr)
                label=flagArr[1]
            result[item[0]] =  label

        # print(json)

        return result, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(getFlag, '/v1.0/getFlag/<startTime>/<endTime>/')