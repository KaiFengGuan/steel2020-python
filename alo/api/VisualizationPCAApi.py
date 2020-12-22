'''
VisualizationPCAApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
from ..utils import getData
from ..utils import getFlagArr
from ..utils import SQLplateselect
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
        # return {'hello': 'world'}
        tocSelect = [startTime, endTime]
 
        ismissing = {'all_processes_statistics_ismissing':True,'cool_ismissing':True,'fu_temperature_ismissing':True,'m_ismissing':True,'fqc_ismissing':True} 
        # data = getData(['upid', 'platetype','toc', 'tgtwidth','tgtlength','tgtthickness','all_processes_statistics','fqc_label'], ismissing, [], [], [], tocSelect, [], [], '', '')
        data=SQLplateselect(['d.upid', 'm.productcategory','d.toc', 'd.tgtwidth','d.tgtlength','d.tgtthickness','d.all_processes_statistics','d.fqc_label'],ismissing, [], [], [], tocSelect, [], [], '', '')
        # print(data)
        VisualizationPCAdata = getVisualizationPCA()
        jsondata=VisualizationPCAdata.run(data)
        # credentials = pika.PlainCredentials('guest', 'guest')
        # parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        # connection = pika.BlockingConnection(parameters)
        # channel = connection.channel()

        # connection = pika.BlockingConnection(parameters)
        # channel = connection.channel()

        # channel.queue_declare(queue='BS-endModel', durable=True)

        # channel.basic_publish(exchange='',
        #                     routing_key='BS-endModel',
        #                     body=json.dumps(jsondata),
        #                     properties=pika.BasicProperties(
        #                         delivery_mode=2, # make message persistent
        #                     )
        #                     )
        # print(" [x]BS-endModel:")
        # connection.close()
        # return
        return jsondata, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(VisualizationPCA, '/v1.0/model/VisualizationPCA/<startTime>/<endTime>/')