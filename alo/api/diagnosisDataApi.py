'''
dataPre
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
from ..controller.baogangPlot.createDiagResu import createDiagResu
import pika, traceback
import pandas as pd
import numpy as np
import os
# path = os.getcwd()
parser = reqparse.RequestParser(trim=True, bundle_errors=True)
# path1=os.path.abspath('.') + 'wide_117_data_flag_20190831.csv'
# path2=os.path.abspath('.') + 'steelspec_data20180902.csv'
# filePath1 = r'D:\document\BAOGANGDATA\wide_117_data_flag_20190831.csv'
# def getData():
#     filePath1 = "/usr/src/data/mother_fqc_before/13.csv"
#     # "/usr/src/data/mother_fqc_before/" + upid + ".csv"
#     # filePath1 = r'/alo/data/wide_117_data_flag_20190831.csv'
#     # filePath2 = r'D:\document\BAOGANGDATA\steelspec_data20180902.csv'
#     filePath2 = "/usr/src/data/mother_fqc_before/12.csv"
#     # filePath2 = r'/alo/data/steelspec_data20180902.csv'

    
#     wideData_dir = pd.read_csv("/usr/src/data/mother_fqc_before/13.csv")
#     # wideData_dir = pd.read_csv(filePath1)
#     wideData_dir = wideData_dir.drop_duplicates(['upid'], keep='last').reset_index().drop(['index'], axis=1)
#     wideData_dir[['upid']] = wideData_dir[['upid']].astype('str')
#     wideData_dir = wideData_dir.set_index('upid')
#     wideData = wideData_dir.dropna()
#     # data = pd.read_csv(filePath2)
#     data = pd.read_csv("/usr/src/data/mother_fqc_before/12.csv")
#     data = data.drop_duplicates(['upid'], keep='last').reset_index().drop(['index'], axis=1)
#     data[['upid']] = data[['upid']].astype('str')
#     data[['upid']] = data[['upid']].astype('str')
#     data = data.set_index('upid')
#     result = {
#         'data': data,
#         'wideData': wideData
#     }
#     return result

# # 根目录
# @app.route('/')


class diagnosisDataApi(Resource):
    '''
    diagnosisDataApi
    '''
    def post(self):
        """ 
        post
        ---
        tags:
            - 诊断视图数据
        parameters:
            - in: body
              name: body
              schema:
              properties:
                  upid:
                #   type: string
                #   default: 1
                #   description: 数据预处理
                #   task_id:
                #   type: string
                #   default: 1
                #   description: 任务id
              required: true
        responses:
          200:
            description: 执行成功
        """
        parser.add_argument("upid", type=str, required=True)
        parser.add_argument("width", type=str, required=True)
        parser.add_argument("length", type=str, required=True)
        parser.add_argument("thickness", type=str, required=True)
        parser.add_argument("platetype", type=str, required=True)
        args = parser.parse_args(strict=True)
        upid = args["upid"]

        width = float(args["width"])
        length = float(args["length"])
        thickness = float(args["thickness"])
        platetype=json.loads(args["platetype"])

        result =  []
        outOfGau = {}
        PCAT2 = {}
        PCASPE = {}
        steeldata={}
        try:
            createDiagResu_instance = createDiagResu(upid)
            result, PCAT2, PCASPE = createDiagResu_instance.run(width, length, thickness)
# used to fix remote data
            # createDiagResu_instance = createDiagResu(upid, startTime, endTime)
            # result, outOfGau, PCAT2, PCASPE = createDiagResu_instance.run()

        except Exception:
            print('fhiosif')
            print(traceback.format_exc())
        return {'result': result, 'PCAT2': PCAT2, 'PCASPE': PCASPE}, 200, {'Access-Control-Allow-Origin': '*'}

api.add_resource(diagnosisDataApi, '/v1.0/baogangPlot/diagnosesdata')
