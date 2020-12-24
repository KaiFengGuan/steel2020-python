'''
VisualizationMDSApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData,SQLLabel,data_filter
from ..utils import SQLplateselect
from ..controller.VisualizationMDSController import getVisualizationMDS

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class VisualizationMDS(Resource):
    '''
    SixDpictureUpDownQuantile
    '''
    def get(self,startTime,endTime):
        """
        get
        ---
        tags:
          - 可视化马雷图部分MDS
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
        # return {'hello': 'world'}
        tocSelect = [startTime, endTime]
        ismissing = {'dd.all_processes_statistics_ismissing':'0','dd.cool_ismissing':'0','dd.fu_temperature_ismissing':'0','dd.m_ismissing':'0','dd.fqc_ismissing':'0'} 
        data,col_names = SQLLabel(['dd.all_processes_statistics','dd.fqc_label'],ismissing, [], [], [], tocSelect, [], [], '', '')
        
        data,processdata = data_filter(data,col_names)
        VisualizationMDS = getVisualizationMDS()
        json=VisualizationMDS.run(data,processdata)

        return json, 200, {'Access-Control-Allow-Origin': '*'}

api.add_resource(VisualizationMDS, '/v1.0/model/VisualizationMDS/<startTime>/<endTime>/')