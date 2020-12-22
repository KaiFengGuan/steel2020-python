'''
plateYieldStaisticsApi
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
# from ..controller.modelTransferCsvController import modelTransferCsvController
# from ..controller.getPlateYieldStaisticsAndFlagController import getDataPlateAndFlagCRAndFqc
from ..controller.getPlateYieldStaisticsAndFlagController import getDataPlateYieldAndFlag
from ..utils import getData
from ..utils import getFlagArr
from ..utils import ref
import pandas as pd
parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class plateYieldStaistics(Resource):
    '''
    plateYieldStaistics
    '''
    def get(self,timeDiff,startTime,endTime):
        """
        get
        ---
        tags:
            - 时间线图
        parameters:
            - in: path
              name: timeDiff
              required: true
              description: 时间间隔
              type: string
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

        timeDiff = int(timeDiff)

        # DataPlateAndFlagCRAndFqc = getDataPlateAndFlagCRAndFqc(startTime,endTime)
        # modelFit = DataPlateAndFlagCRAndFqc.run()




        # modelFit is the data read from database
        # tocSelect=['2018-12-01 01:41:43','2018-12-10 12:11:43']
        tocSelect = [startTime, endTime]
        ismissing={'all_processes_statistics_ismissing':True,'cool_ismissing':True,'fu_temperature_ismissing':True,'m_ismissing':True,'fqc_ismissing':True} 
        data = getData(['upid', 'toc', 'fqc_label'], ismissing, [], [], [], tocSelect, [], [], '', '')
        modelFit = {
          'toc': [],
          'upid': [],
          'flag': []
        }
        for item in  data:
          msum = 0
          modelFit['toc'].append(item[1])
          modelFit['upid'].append(item[0])
          flagArr = getFlagArr(item[2]['method1'])
          for label in flagArr:
            msum = msum + label
          if (msum >= ref):
            modelFit['flag'].append(1)
          else:
            modelFit['flag'].append(0)
        modelFit = pd.DataFrame(modelFit)
        # print(modelFit['flag'].shape)
        PlateYieldStaistics = getDataPlateYieldAndFlag(startTime,endTime)
        good_flag,bad_flag,endTimeOutput = PlateYieldStaistics.run(timeDiff, modelFit)
        # good_flag,bad_flag,endTimeOutput = PlateYieldStaistics.run(timeDiff,modelFit)


        return {'endTimeOutput': endTimeOutput,'good_flag': good_flag,'bad_flag': bad_flag,}, 200, {'Access-Control-Allow-Origin': '*'}



api.add_resource(plateYieldStaistics, '/v1.0/model/plateYieldStaistics/<timeDiff>/<startTime>/<endTime>/')
