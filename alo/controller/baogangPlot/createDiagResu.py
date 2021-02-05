'''
createDiagResu
'''
# https://scikit-learn.org/stable/modules/preprocessing.html#scaling-features-to-a-range
import pandas as pd
import numpy as np
import json
from sklearn import preprocessing
import scipy.io as scio
from scipy.stats import f
from scipy.stats import norm
from ...methods.baogangPlot.PCA import PCATEST
from ...utils import SQLplateselect
from ...methods.baogangPlot.dataInKind import dataInKind
from ...methods.baogangPlot.setKindMethod import setKindMethod
from ...utils import getFlagArr,getData,SQLLabel,unidimensional_monitoring,data_filter
import datetime
class createDiagResu:
    '''
    createDiagResu
    '''

    def __init__(self, upid):
        self.upid = upid
        self.paramsIllegal = False
        try:
            # 如果以后加入参数，在这里加入
            print('createDiagResu方法暂时没有参数')
        except Exception:
            self.paramsIllegal = True

    def run(self, width, length, thickness,platetype):
        '''
        run
        '''

        Platetypes=platetype
        if(platetype[0]=='All'):
            Platetypes=[]
        else:
            Platetypes=platetype
        
        ismissing = {'dd.all_processes_statistics_ismissing':'0','dd.cool_ismissing':'0','dd.fu_temperature_ismissing':'0','dd.m_ismissing':'0','dd.fqc_ismissing':'0'} 
        platedata,col_names = SQLLabel(['dd.fqc_label'],ismissing, [], [], [], [], [self.upid], [], '', '')
        data =  pd.DataFrame(data = platedata, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
        dataLabel = 0
        data=data.values
        # print(len(data))
        # print(len(data[0]))
        dataFlag = getFlagArr(data[0][134]['method1'])
        dataAmount=0
        for j in dataFlag:
            dataAmount+=j
        if(dataAmount>=3):
            dataLabel = 1
        time = data[0][4]
        delta = datetime.timedelta(days = 365)
        start = str(time - delta)
        end = str(time +delta)

        otherWidth = [str(data[0][6] - width), str(data[0][6] + width)]
        otherLen = [str(data[0][7] - length), str(data[0][7] + length)]
        otherThick = [str(data[0][5] - thickness), str(data[0][5] + thickness)]
        otherSelectTime = [start, end]
        otherdata,col_names = SQLLabel(['dd.fqc_label'],ismissing, otherWidth, otherLen, otherThick, otherSelectTime, [], Platetypes, 'toc', '')
        otherdata =  pd.DataFrame(data = otherdata, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
        raw_process_data = otherdata[col_names[5:134]]
        otherdata = otherdata[((raw_process_data < 1e+10) & (raw_process_data > -1e+10)).sum(axis=1) == raw_process_data.shape[1]].reset_index(drop = True)
        otherData=otherdata.values
        labelArr = []
        badBoardData = []
        goodBoardData = []
        badBoardId = []
        goodBoardId = []
        
        for item in otherData:
            flagArr = getFlagArr(item[134]['method1'])
            label=0
            amount=0
            for j in flagArr:
                amount+=j
            if(amount>=3):
                label=1
            labelArr.append(label)
            if (label > 0):
                badBoardId.append(item[1])
                badBoardData.append(item[13:134].astype(np.float32))
            else:
                goodBoardId.append(item[1])
                goodBoardData.append(item[13:134].astype(np.float32))
        if (dataLabel == 1):
            badBoardId.append(data[0][1])
            badBoardData.append(data[0][13:134].astype(np.float32))
        else:
            goodBoardId.append(data[0][1])
            goodBoardData.append(data[0][13:134].astype(np.float32))
        badBoardData = np.array(badBoardData)
        goodBoardData = np.array(goodBoardData)
        print(otherdata.shape)
        print(goodBoardData.shape)
        allBoardId = goodBoardId + badBoardId
        colonmName = col_names[13:134]
        startAddress = 0
        endAddress = -1
        dataName = colonmName[startAddress:endAddress]
        goodBoardData=goodBoardData[:,startAddress:endAddress]
        badBoardData=badBoardData[:,startAddress:endAddress]
        # allBoardData=allBoardData[:,startAddress:endAddress]
        # print(goodBoardData.shape)
        # print(np.argwhere(np.isnan(np.array(goodBoardData))))
        # print(np.argwhere(np.isfinite(np.array(goodBoardData))))

        
        # # print(np.argwhere(np.isnan(np.array(goodBoardData))))
        # # print(np.argwhere(np.isfinite(np.array(goodBoardData))))
        # print(colonmName[72])
        # return goodBoardData.tolist()


        goodSta = np.mean(goodBoardData, axis=0)
        scaler = preprocessing.StandardScaler().fit(goodBoardData)
        X_mean = scaler.mean_
        X_std = scaler.scale_
        X_up = scaler.mean_+ scaler.scale_
        X_down = scaler.mean_- scaler.scale_
        scalerGood = scaler.transform(goodBoardData)
        scalerBad = scaler.transform(badBoardData)
        dataProUp = scaler.transform(np.array([X_up]))
        dataProDown = scaler.transform(np.array([X_down]))
        dataMean = np.mean(scalerGood,axis=0)
        min_max_scaler = preprocessing.MinMaxScaler()
        maxminGood = min_max_scaler.fit_transform(scalerGood)
        maxminBad = min_max_scaler.transform(scalerBad)
        allMaxMin = np.concatenate((maxminGood, maxminBad), axis=0)
        dataMeanMinmax = min_max_scaler.transform(np.array([dataMean]))
        dataProUp = min_max_scaler.transform(dataProUp)[0,:]
        dataProDown = min_max_scaler.transform(dataProDown)[0,:]
        X_test = np.array(badBoardData)
        X_train = np.array(goodBoardData)
        X_zero_std = np.where(np.std(X_train, axis=0)==0)
        # for i in X_zero_std[0]:
        #     del outDataCol[i]
        X_train = np.delete(X_train, X_zero_std, axis=1)
        X_test = np.delete(X_test, X_zero_std, axis=1)
        # for item in allZeroList:
        #     del outDataColCopy[item]
        X_all = np.vstack((X_train,X_test))
        idToPlot = self.upid
        # position = [allBoardId.index(item) for item in idToPlot]
        position = allBoardId.index(idToPlot)
        # print(allMaxMin[position,:]-dataProUp)
        # print(allMaxMin[position,:]-dataProDown)
        upDis = [0 if item<=0 else item for item in allMaxMin[position,:]-dataProUp]
        lowDis = [0 if item>=0 else item for item in allMaxMin[position,:]-dataProDown]
        barData  = np.array(upDis) + np.array(lowDis)
        # print(barData)
        barDataPer = np.abs(barData)/(np.array(dataProUp)-np.array(dataProDown))*100
        T2UCL1, T2UCL2, QUCL, T2, Q, CONTJ, contq = PCATEST().general_call({
            'Xtrain': X_train,
            'Xtest': X_test,
            'testNum': position
            })
        result = []
        CONTJ_Pro = []
        maxCON = max(CONTJ)
        minCON = min(CONTJ)
        for item in CONTJ:
            mid =  (item - minCON)/(maxCON - minCON) *6
            CONTJ_Pro.append(mid)

        contq_Pro = []
        maxContq = max(contq.tolist())
        minContq = min(contq.tolist())
        for item in contq.tolist():
            mid =  (item - minContq)/(maxContq - minContq) *6
            contq_Pro.append(mid)
        outOfGau = {
            'xData': dataName,
            'sData': barDataPer.tolist()
        }
        PCAT2 = {
            'xData': dataName,
            'sData': CONTJ_Pro
        }
        PCASPE = {
            'xData': dataName,
            'sData': contq_Pro
        }
        for i in range(len(allMaxMin[position].tolist())):
            result.append({
                'value': allMaxMin[position].tolist()[i],
                'name': dataName[i],
                'l': dataProDown[i],
                'u': dataProUp[i]
            })
        goodBoardId.append(data[0][1])
        otherdata=otherdata[otherdata["upid"].isin(goodBoardId)]
        result=unidimensional_monitoring(data[0][1], otherdata, 0.25,col_names)
        steel=data[0][1:11]
        steel[3]=str(steel[3])
        steel=steel.tolist()
        labels=col_names[1:11]
        # del steel[3]
        # del labels[3]
        del steel[2]
        del labels[2]
        return result, outOfGau, PCAT2, PCASPE,{'labels':labels,'steel':steel}
