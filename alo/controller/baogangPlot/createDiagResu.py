'''
createDiagResu
'''
# https://scikit-learn.org/stable/modules/preprocessing.html#scaling-features-to-a-range
import pandas as pd
import numpy as np
import json
from scipy.stats import f
import scipy.io as scio
from scipy.stats import norm
from ...utils import getFlagArr,getData,SQLLabel

class PCATEST:
    '''
    PCATEST
    '''

    def __init__(self):
        self.paramsIllegal = False
        try:
            # 如果以后加入参数，在这里加入
            print('PCATEST方法暂时没有参数')
        except Exception:
            self.paramsIllegal = True

    def general_call(self, custom_input):
        '''
        general_call
        '''
        Xtrain = custom_input['Xtrain']
        Xtest  = custom_input['Xtest']
        X_row  = Xtrain.shape[0]
        X_col  = Xtrain.shape[1]
        X_mean = np.mean(Xtrain, axis=0)
        X_std  = np.std(Xtrain, axis=0)
        Xtrain = (Xtrain - np.tile(X_mean, (X_row, 1))) / np.tile(X_std, (X_row, 1))
        
        sigmaXtrain = np.cov(Xtrain.T)
        [lamda, T] = np.linalg.eigh(sigmaXtrain)
        num_pc = 1
        D = -np.sort(-lamda, axis=0)
        lamda = np.diag(lamda)
        while D[0:num_pc].sum(axis=0) / D.sum(axis=0) < 0.9:
            num_pc = num_pc + 1
        P = T[:, np.arange(X_col - num_pc, X_col)]
        T2UCL1 = num_pc * (X_row - 1) * (X_row + 1) * f.ppf(0.99, num_pc, X_row - num_pc) / (X_row * (X_row - num_pc))
        T2UCL2 = num_pc * (X_row - 1) * (X_row + 1) * f.ppf(0.95, num_pc, X_row - num_pc) / (X_row * (X_row - num_pc))
        theta = np.zeros(3)
        for i in range(3):
            theta[i] = np.sum((D[np.arange(num_pc, X_col)]) ** (i + 1))
        h0 = 1 - 2 * theta[0] * theta[2] / (3 * theta[1] ** 2)
        ca = norm.ppf(0.99, 0, 1)
        QUCL = theta[0] * (
                    h0 * ca * np.sqrt(2. * theta[1]) / theta[0] + 1 + theta[1] * h0 * (h0 - 1.) / theta[0] ** 2.) ** (
                        1. / h0)
        n = Xtest.shape[0]
        m = Xtest.shape[1]
        XtrainTest = (Xtest - np.tile(X_mean, (n, 1))) / np.tile(X_std, (n, 1))
        X = np.concatenate((Xtrain,XtrainTest),axis=0)  
        P = np.matrix(P)
        [r, y] = (P * P.T).shape
        I = np.eye(r, y)
        T2 = np.zeros((n, 1))
        Q = np.zeros((n, 1))
        for i in range(n):
            T2[i] = np.matrix(X[i, :]) * P * np.matrix(
                (lamda[np.ix_(np.arange(m - num_pc, m), np.arange(m - num_pc, m))])).I * P.T * np.matrix(X[i, :]).T
            
            Q[i] = np.matrix(X[i, :]) * (I - P * P.T) * np.matrix(X[i, :]).T
            
        test_Num = 0
        S = np.array(np.matrix(X[test_Num, :]) * P[:, np.arange(0, num_pc)])
        S = S[0]
        r = []
        for i in range(num_pc):
            if S[i] ** 2 / lamda[i, 0] > T2UCL1 / num_pc:
                r.append(i)
        cont = np.zeros((len(r), m))
        for i in [len(r) - 1]:
            for j in range(m):
                cont[i][j] = np.fabs(S[i] / D[i] * P[j, i] * X[test_Num, j])

        CONTJ = []
        for j in range(m):
            CONTJ.append(np.sum(cont[:, j]))
        e = np.matrix(X[test_Num, :]) * (I - P * P.T)
        e = np.array(e)[0]
        contq = e ** 2
        return T2UCL1, T2UCL2, QUCL, T2, Q, CONTJ, contq

def unidimensional_monitoring(upid, data, quantile_num, extremum_quantile_num, col_names):
    ##根据upid查询该钢板近一年的同类型数据
    data = data #这里省略，调用封装好的同类型钢板查询接口即可
    data_columns = data.columns.values
    ## 获取同一规格钢板的取过程数据
    process_data = data[col_names[13:134]]
    ## 计算原始过程数据的上下分位点
    lower_limit  = process_data.quantile(q = quantile_num, axis = 0).values
    upper_limit  = process_data.quantile(q = 1-quantile_num, axis = 0).values
    ## 计算原始过程数据的上下极值分位点
    extremum_lower_limit  = process_data.quantile(q = extremum_quantile_num, axis = 0).values
    extremum_upper_limit  = process_data.quantile(q = 1-extremum_quantile_num, axis = 0).values
    ## 查询此钢板的过程数据（若前端在点击马雷图或散点图前已经储存该数据，则此步骤可以省略）
    upid_data = data[data.upid == upid][col_names[13:134]].values[0]
    
    ## 对同一规格钢板过程数据进行归一化计算
    norm_process_data = (process_data - process_data.min()) / (process_data.max() - process_data.min())
    ## 计算归一化后过程数据的上下分位点
    lower_limit_norm = norm_process_data.quantile(q = quantile_num, axis = 0).values
    upper_limit_norm = norm_process_data.quantile(q = 1-quantile_num, axis = 0).values
    ## 计算归一化后过程数据的上下极值分位点
    extremum_lower_limit_norm = norm_process_data.quantile(q = extremum_quantile_num, axis = 0).values
    extremum_upper_limit_norm = norm_process_data.quantile(q = 1-extremum_quantile_num, axis = 0).values
    ## 查询此钢板归一化后的过程数据
    norm_upid_data = norm_process_data[data.upid == upid][col_names[13:134]].values[0]
    
    #数据合并至Json
    # unidimensional_monitoring_data={}
    # unidimensional_monitoring_data['data_columns']=data_columns.tolist()
    result=[]
    labels=col_names[13:134]
    for i in range(len(labels)):
        result.append({
            'name': labels[i],
            'value': norm_upid_data[i],
            'l': lower_limit_norm[i],
            'u': upper_limit_norm[i],
            'extremum_l':extremum_lower_limit_norm[i],
            'extremum_u':extremum_upper_limit_norm[i],
            'original_value':upid_data[i],
            'original_l':lower_limit[i],
            'original_u':upper_limit[i],
            'extremum_original_l':extremum_lower_limit[i],
            'extremum_original_u':extremum_upper_limit[i]
            })
    return result    


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

    def run(self, width, length, thickness):
        '''
        run
        '''
        print(self.upid)
        ismissing = {'dd.all_processes_statistics_ismissing':'0','dd.cool_ismissing':'0','dd.fu_temperature_ismissing':'0','dd.m_ismissing':'0','dd.fqc_ismissing':'0'} 
        platedata,col_names = SQLLabel(['dd.fqc_label'],ismissing, [], [], [], [], [self.upid], [], '', '')
        platedata =  pd.DataFrame(data = platedata, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
        # col_names = raw_data.columns.values
        # platedata = raw_data[raw_data['upid'] == self.upid]
        # plate_category = platedata.productcategory.values
        data =  pd.DataFrame(data = platedata, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
        data.fqc_label = data.fqc_label.map(lambda x : getFlagArr(x['method1'])[1])
        data = data.values

        otherWidth = [str(data[0][6] - width), str(data[0][6] + width)]
        otherLen   = [str(data[0][7] - length), str(data[0][7] + length)]
        otherThick = [str(data[0][5] - thickness), str(data[0][5] + thickness)]
        otherCategory = platedata.productcategory.values[0]
        # otherdata = raw_data[(float(otherThick[0])<raw_data['tgtplatethickness2']) & (raw_data['tgtplatethickness2']<float(otherThick[1]))
        #                    & (float(otherWidth[0])<raw_data['tgtwidth']) & (raw_data['tgtwidth']<float(otherWidth[1])) 
        #                    & (float(otherLen[0])<raw_data['tgtplatelength2']) & (raw_data['tgtplatelength2']<float(otherLen[1]))
        #                    & (otherCategory == raw_data['productcategory'])]
        otherdata,col_names = SQLLabel(['dd.fqc_label'],ismissing, otherWidth, otherLen, otherThick, [], [], otherCategory, 'toc', '')
        otherdata =  pd.DataFrame(data = otherdata, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
        
        if(len(otherdata[otherdata.fqc_label == 1]) < 100):
            thickness = 0.01
            width = 0.1 
            length = 5
            otherThick= [str(data[0][5] - thickness), str(data[0][5] + thickness)]
            # otherdata = raw_data[(float(otherThick[0])<raw_data['tgtplatethickness2']) & (raw_data['tgtplatethickness2']<float(otherThick[1]))
            #                & (float(otherWidth[0])<raw_data['tgtwidth']) & (raw_data['tgtwidth']<float(otherWidth[1])) 
            #                & (float(otherLen[0])<raw_data['tgtplatelength2']) & (raw_data['tgtplatelength2']<float(otherLen[1]))]
            otherdata,col_names = SQLLabel(['dd.fqc_label'],ismissing, otherWidth, otherLen, otherThick, [], [], [], 'toc', '')
            otherdata =  pd.DataFrame(data = otherdata, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
        otherdata.fqc_label = otherdata.fqc_label.map(lambda x : getFlagArr(x['method1'])[1])
        print(len(otherdata))
        print(len(otherdata[otherdata.fqc_label == 1]))
        print("egudfu")
        raw_process_data = otherdata[col_names[5:134]]
        otherdata = otherdata[((raw_process_data < 1e+10) & (raw_process_data > -1e+10)).sum(axis=1) == raw_process_data.shape[1]].reset_index(drop = True)
        otherList = otherdata.values
        
        labelArr  = []
        badBoardData  = []
        goodBoardData = []     
        for item in otherList:
            label = item[134]
            labelArr.append(label)
            if (label == 0):
                badBoardData.append(item[13:134].astype(np.float32))
            else:
                goodBoardData.append(item[13:134].astype(np.float32))
                
        goodBoardData = np.array(goodBoardData)
        platedata = platedata.values[0][13:134].astype(np.float32)
        plateBoardData = platedata[np.newaxis,:]
        dataName = col_names[13:134]

        X_test = np.array(plateBoardData)
        X_train = np.array(goodBoardData)
        X_zero_std = np.where(np.std(X_train, axis=0)==0)
        X_train = np.delete(X_train, X_zero_std, axis=1)
        X_test = np.delete(X_test, X_zero_std, axis=1)
        
        T2UCL1, T2UCL2, QUCL, T2, Q, CONTJ, contq = PCATEST().general_call({
            'Xtrain': X_train,
            'Xtest': X_test
            })
        result = []
        CONTJ_Pro = []
        maxCON = max(CONTJ)
        minCON = min(CONTJ)
        for item in CONTJ:
            mid =  (item - minCON)/(maxCON - minCON)
            CONTJ_Pro.append(mid)

        contq_Pro = []
        maxContq = max(contq.tolist())
        minContq = min(contq.tolist())
        for item in contq.tolist():
            mid =  (item - minContq)/(maxContq - minContq)
            contq_Pro.append(mid)
        PCAT2 = {
            'xData': dataName,
            'sData': CONTJ_Pro
        }
        PCASPE = {
            'xData': dataName,
            'sData': contq_Pro
        }
        goodBoardDf = pd.DataFrame(data = otherdata[otherdata.fqc_label == 1], columns = col_names).reset_index(drop = True)
        print(goodBoardDf.shape)
        goodBoardDf = goodBoardDf.append(otherdata[otherdata['upid'] == self.upid]).reset_index(drop = True)
        print(goodBoardDf.shape)
        result=unidimensional_monitoring(self.upid, goodBoardDf, 0.25, 0.1, col_names)
        return result, PCAT2, PCASPE