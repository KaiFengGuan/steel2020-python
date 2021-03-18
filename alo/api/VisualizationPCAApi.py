'''
VisualizationPCAApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData,SQLplateselect,SQLLabel,data_filter,getData
from ..controller.VisualizationPCAController import getVisualizationPCA
import pika, traceback

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class VisualizationPCA(Resource):
    '''
    SixDpictureUpDownQuantile
    '''
    def get(self,startTime,endTime):
        """
        get
        ---
        tags:
          - 可视化马雷图部分PCA
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
        data,col_names = SQLLabel(['dd.fqc_label'],ismissing, [], [], [], tocSelect, [], [], '', '')
        
        data,processdata = data_filter(data,col_names)
        VisualizationPCAdata = getVisualizationPCA()
        jsondata=VisualizationPCAdata.run(data,processdata,col_names)
        return jsondata, 200, {'Access-Control-Allow-Origin': '*'}

api.add_resource(VisualizationPCA, '/v1.0/model/VisualizationPCA/<startTime>/<endTime>/')