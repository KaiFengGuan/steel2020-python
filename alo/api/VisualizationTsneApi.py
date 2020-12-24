'''
VisualizationTsneApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData,SQLplateselect,SQLLabel,data_filter
from ..controller.VisualizationTsneController import getVisualizationTsne

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class VisualizationTsne(Resource):
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
        data,col_names = SQLLabel(['dd.all_processes_statistics','dd.fqc_label'],ismissing, [], [], [], tocSelect, [], [], '', '')
        data,processdata = data_filter(data,col_names)
        VisualizationTsne = getVisualizationTsne()
        json=VisualizationTsne.run(data,processdata)

        return json, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(VisualizationTsne, '/v1.0/model/VisualizationTsne/<startTime>/<endTime>/')