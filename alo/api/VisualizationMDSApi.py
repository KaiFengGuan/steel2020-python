'''
VisualizationMDSApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData
from ..utils import getFlagArr
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
        print(tocSelect)
        ismissing = {'all_processes_statistics_ismissing':True,'cool_ismissing':True,'fu_temperature_ismissing':True,'m_ismissing':True,'fqc_ismissing':True} 
        # data = getData(['upid', 'platetype','toc', 'tgtwidth','tgtlength','tgtthickness','all_processes_statistics','fqc_label'], ismissing, [], [], [], tocSelect, [], [], '', '')
        data=SQLplateselect(['d.upid', 'm.productcategory','d.toc', 'd.tgtwidth','d.tgtlength','d.tgtthickness','d.all_processes_statistics','d.fqc_label'],ismissing, [], [], [], tocSelect, [], [], '', '')
        # print(data)
        VisualizationMDS = getVisualizationMDS()
        json=VisualizationMDS.run(data)
        # print(json)

        return json, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(VisualizationMDS, '/v1.0/model/VisualizationMDS/<startTime>/<endTime>/')