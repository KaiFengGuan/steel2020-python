'''
modelTransferController
'''
import pandas as pd
import requests
import json
# from .getDataController import getDataController
from .dataFilterController import dataFilterController
# from .dataFilterAfter import dataFilterAfter
# from controller.deepCNNSinTestController import deepCNNSinTestController
# from .deepCNNTestController import deepCNNTestController
import datetime
import math
import os
# from ..staticPath import staticPath

# class getDataPlateAndFlagCRAndFqc:
    # '''
    # getDataPlateAndFlagCRAndFqc
    # '''

    # def __init__(self, startTime, endTime):
    #     self.startTime = startTime
    #     self.endTime = endTime

    # def run(self):
    #     '''
    #     run
    #     '''
    #     path = os.getcwd()

    #     startTime = self.startTime
    #     endTime = self.endTime

    #     api = 'http://java-serve:8080/web-ssm/myf/L2PlateYieldStaistics/selectL2PlateYieldStaisticsAndCRflag/all/'+startTime+'/'+endTime+'/'
    #     PlateStaisticCRflagTime = requests.get(api)
    #     PlateStaisticCRflagTime = pd.DataFrame(json.loads(PlateStaisticCRflagTime.content))

    #     data_usid = pd.read_csv(path + staticPath.data_tag_w)
    #     # data_usid = pd.read_csv(path + staticPath.data_tag_l)
    #     data_usid_np = data_usid['Unnamed: 0'].values
    #     Newtag1 = data_usid['Newtag1'].values
    #     start_flag = 0
    #     upid = []
    #     upid_flag_list = []

    #     for i in range(len(data_usid_np) - 1):
    #         if (i == len(data_usid_np) - 1) | (data_usid_np[i][0:8] != data_usid_np[i + 1][0:8]):
    #             #         print(i)
    #             end_flag = i

    #             upid.append(data_usid_np[i][0:8] + "000")

    #             usid_num = end_flag - start_flag + 1
    #             upid_flag = 1
    #             for j in range(usid_num):
    #                 if (Newtag1[start_flag + j] == 0):
    #                     upid_flag = 0
    #             #             print(upid_flag)
    #             upid_flag_list.append(upid_flag)

    #             start_flag = end_flag + 1

    #     upid_df = pd.DataFrame(upid, columns=['upid'])
    #     upid_flag_df = pd.DataFrame(upid_flag_list, columns=['upid_flag'])
    #     flag_df = pd.concat([upid_df, upid_flag_df], axis=1)

    #     upid_CR_FQC = pd.merge(PlateStaisticCRflagTime, flag_df, on='upid', how='left')
    #     upid_FQC = upid_CR_FQC.dropna(axis=0, how='any')[['upid', 'upid_flag','toc']]
    #     upid_FQC.columns = ['upid', 'flag','toc']
    #     upid_CR = upid_CR_FQC[upid_CR_FQC.isnull().values == True][['upid', 'crflag','toc']]
    #     upid_CR.columns = ['upid', 'flag','toc']

    #     upid_CR_FQC_finish = upid_FQC.append(upid_CR).sort_index(axis=0, ascending=True)


    #     return upid_CR_FQC_finish


class getDataPlateYieldAndFlag:
    '''
    getDataPlateYieldAndFlag
    '''

    def __init__(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime

    def run(self,timeDiff,upid_CR_FQC):
        '''
        run
        '''
        startTime = datetime.datetime.strptime(self.startTime, '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(self.endTime, '%Y-%m-%d %H:%M:%S')

        hours = math.ceil((endTime - startTime).total_seconds() // 3600 / timeDiff)
        upid_CR_FQC['toc'] = pd.to_datetime(upid_CR_FQC['toc'], format='%Y-%m-%d %H:%M:%S')

        startPostion = startTime
        if hours == 1:
            endPostion = endTime
        else:
            endPostion = startTime + datetime.timedelta(hours=timeDiff)

        good_flag = []
        bad_flag = []
        endTimeOutput = []

        for i in range(hours):
            # print(upid_CR_FQC['flag'] == 1)
            good_flag.append(len(upid_CR_FQC[(upid_CR_FQC['toc'] > startPostion) & (upid_CR_FQC['toc'] < endPostion) & (upid_CR_FQC['flag'] == 0)]))
            bad_flag.append(len(upid_CR_FQC[(upid_CR_FQC['toc'] > startPostion) & (upid_CR_FQC['toc'] < endPostion) & (upid_CR_FQC['flag'] == 1)]))

            endTimeOutput.append(str(endPostion))


            startPostion = endPostion
            if i == hours - 1:
                endPostion = endTime
            else:
                endPostion = startPostion + datetime.timedelta(hours=timeDiff)


        return good_flag,bad_flag,endTimeOutput

# instance = modelTransferController('2018-09-01 00:00:00', '2018-09-02 00:00:00')
# instance.run()