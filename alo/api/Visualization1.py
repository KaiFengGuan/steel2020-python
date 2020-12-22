'''
Visualization
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
import numpy as np
from ..utils import getData
from ..utils import getFlagArr
import json
from sklearn.decomposition import PCA
from scipy.interpolate import interp1d

parser = reqparse.RequestParser(trim=True, bundle_errors=True)

# # 根目录
# @app.route('/')


class Visualization(Resource):
    '''
    SixDpictureUpDownQuantile
    '''
    def get(self,upid,process,width,length,thickness,platetype):
        """
        get
        ---
        tags:
          - 可视化
        parameters:
            - in: path
              name: upid
              required: true
              description: 钢板upid
              type: string
            - in: path
              name: process
              required: true
              description: process
              type: string
            - in: path
              name: width
              required: true
              description: width
              type: number
            - in: path
              name: length
              required: true
              description: length
              type: number
            - in: path
              name: thickness
              required: true
              description: thickness
              type: number
            - in: path
              name: platetype
              required: true
              description: platetype
              type: string
        responses:
            200:
                description: 执行成功
        """
        def eyearray(tempnum):
          return np.linspace(0,10*np.pi,num=tempnum)     
        def scipyutils(num,x_diff):
          x=eyearray(num)
          y=x_diff
          x_diff=eyearray(len(x_diff))
          f1=interp1d(x_diff,y,kind='linear')#线性插值
          # f2=interp1d(x_diff,y,kind='cubic')#三次样条插值
          return f1(x)
        UpidSelect=[]
        UpidSelect.append(upid)
        data = getData(['tgtwidth','tgtlength','tgtthickness'], {}, [], [], [], [], UpidSelect, [], '', '')  
        tgtwidthSelect=[repr(data[0][0]-float(width)),repr(data[0][0]+float(width))]
        tgtlengthSelect=[repr(data[0][1]-float(length)),repr(data[0][1]+float(length))]
        tgtthicknessSelect=[repr(data[0][2]-float(thickness)),repr(data[0][2]+float(thickness))]
        ismissing={'all_processes_statistics_ismissing':True,'cool_ismissing':True,'fu_temperature_ismissing':True,'m_ismissing':True,'fqc_ismissing':True}
        selection=[]
        if (process=='cool'):
          selection.append('v1')
          selection.append('v2')
        if (process=='heat'):
          selection.append('v2')
        if (process=='roll'):
          selection.append('v3')
        if(platetype=='All'):
          Platetypes=[]
        else:
            Platetypes=[platetype]
        data = getData(selection, ismissing, tgtwidthSelect, tgtlengthSelect, tgtthicknessSelect, [], [], Platetypes, '', '1000')
        sampledata = getData(selection, {}, [], [], [], [], UpidSelect, [], '', '')
        # print(process)
        jsondata={}
        len1=len(data)

        if (process=='cool'):
          name=['p1',"p2L",'p4','p5','p6']
          nameindex=[]
          coolright=1
          coolleft=1
          for m in range(len(name)):  ##冷却
            nameindex.append(len(json.loads(sampledata[0][0][name[m]])['data']))
            coolKate=[]
            sampletemp=json.loads(sampledata[0][0][name[m]])['data']
            for i in range(len1):
              cooltemp=json.loads(data[i][0][name[m]])['data']
              if(len(cooltemp)>nameindex[m]+coolright):continue
              if(len(cooltemp)<nameindex[m]-coolleft):continue
              while(len(cooltemp)!=nameindex[m]):  #冷却插值
                  cooltemp=scipyutils(nameindex[m],cooltemp)
              coolKate.append(cooltemp)
            # print(len(coolKate))            
            sampletemp=np.array(sampletemp)
            coolKate=np.array(coolKate)
            minroll=np.percentile(coolKate, 30, axis=0)
            maxroll=np.percentile(coolKate, 90, axis=0)
            samplearray=np.concatenate([minroll,maxroll,sampletemp]) 
            jsondata[name[m]]={"min":list(minroll),"max":list(maxroll),'sample':list(sampletemp),"range":[(np.min(samplearray)),np.max(samplearray)]}
          #二维温度场
          name1="Scanner"                
          coolKate=[]
          sampletemp=[]
          nameindex1=len(json.loads(sampledata[0][1]['Scanner'])['data'])
          sampletemp=np.array(json.loads(sampledata[0][1]['Scanner'])['data']).mean(axis=1)
          for i in range(len1):
            cooltemp=np.array(json.loads(data[i][1]['Scanner'])['data']).mean(axis=1)
            cooltemp=list(cooltemp)
            if(len(cooltemp)>nameindex1+coolright):continue
            if(len(cooltemp)<nameindex1-coolleft):continue
            while(len(cooltemp)!=nameindex1):  #冷却插值
              cooltemp=scipyutils(nameindex1,cooltemp)
            coolKate.append(cooltemp)
          coolKate=np.array(coolKate)
          mincool=np.percentile(coolKate, 30, axis=0)
          maxcool=np.percentile(coolKate, 90, axis=0)
          samplearray=np.concatenate([minroll,maxroll,sampletemp]) 
          # mincool = np.round(mincool,2)
          # maxcool = np.round(maxcool,2)
          # samplearray = np.round(samplearray,2)
          jsondata[name1]={"min":list(mincool),"max":list(maxcool),'sample':list(sampletemp),"range":[(np.min(samplearray)),np.max(samplearray)]} 

        if (process=='heat'):
          name=['temp_seg_ul_1','temp_seg_ul_2','temp_seg_dl_s','temp_seg_ur_1','temp_seg_ur_2','temp_seg_dr_s']
          name1="Scanner"
          nameindex=[]         
          heatright=1
          heatleft=1
          for m in range(len(name)):#确定sampledata各项数据的指标
            nameindex.append(len(json.loads(sampledata[0][0]['Fufladc'])['data'][m]))
            heatKate=[]
            sampletemp=json.loads(sampledata[0][0]['Fufladc'])['data'][m]
            for i in range(len1): 
              heattemp=json.loads(data[i][0]['Fufladc'])['data'][m]
              if(len(heattemp)>=nameindex[m]+heatright):continue
              if(len(heattemp)<=nameindex[m]-heatleft):continue
              while(len(heattemp)!=nameindex[m]):  #插值
                heattemp=scipyutils(nameindex[m],heattemp)
              heatKate.append(heattemp)
            # print(len(heatKate))            
            sampletemp=np.array(sampletemp)
            heatKate=np.array(heatKate)
            minroll=np.percentile(heatKate, 30, axis=0)
            maxroll=np.percentile(heatKate, 90, axis=0)
            samplearray=np.concatenate([minroll,maxroll,sampletemp]) 
            jsondata[name[m]]={"min":list(minroll),"max":list(maxroll),'sample':list(sampletemp),"range":[(np.min(samplearray)),np.max(samplearray)]}
          #二维温度场
          heatKate=[]
          sampletemp=[]
          nameindex1=len(json.loads(sampledata[0][0]['Scanner'])['data'])
          sampletemp=np.array(json.loads(sampledata[0][0]['Scanner'])['data']).mean(axis=1)
          for i in range(len1):
            heattemp=np.array(json.loads(data[i][0]['Scanner'])['data']).mean(axis=1)
            heattemp=list(heattemp)
            if(len(heattemp)>nameindex1+heatright):continue
            if(len(heattemp)<nameindex1-heatleft):continue
            while(len(heattemp)!=nameindex1):  #插值
              heattemp=scipyutils(nameindex1,heattemp)
            heatKate.append(heattemp)
          heatKate=np.array(heatKate)
          # print(len(heatKate))
          minheat=np.percentile(heatKate, 30, axis=0)
          maxheat=np.percentile(heatKate, 90, axis=0)
          samplearray=np.concatenate([minroll,maxroll,sampletemp]) 
          # minheat = np.round(minheat,2)
          # maxheat = np.round(maxheat,2)
          # samplearray = np.round(samplearray,2)
          jsondata[name1]={"min":list(minheat),"max":list(maxheat),'sample':list(sampletemp),"range":[(np.min(samplearray)),np.max(samplearray)]}       
        
        if(process=='roll'):
          name=["bendingforce","bendingforcebot","bendingforcetop","rollforce","rollforceds","rollforceos","screwdown","shiftpos","speed","torque","torquebot","torquetop"]
          name1=["contactlength","entrytemperature","exitflatness","exitprofile","exittemperature","exitthickness","exitwidth","forcecorrection"]      
          rollright=1
          rollleft=1
          nameindex=[]
          nameindex1=[]
          def rollfor(name,nameindex,serchkey):
            for m in range(len(name)):#确定sampledata各项数据的指标
              nameindex.append(len(json.loads(sampledata[0][0][serchkey])['data'][m]))
              rollKate=[]
              sampletemp=np.array(json.loads(sampledata[0][0][serchkey])['data'][m]).mean(axis=1)
              for i in range(len1): #n*k*8->n*k(sample)
                rolltemp=list(np.array(json.loads(data[i][0][serchkey])['data'][m]).mean(axis=1)) #k*8->k
                if(len(rolltemp)>nameindex[m]+rollright):
                  continue
                if(len(rolltemp)<nameindex[m]-rollleft):
                  continue
                while(len(rolltemp)<nameindex[m]):
                  rolltemp.append(rolltemp[-1])
                while(len(rolltemp)>nameindex[m]):
                  rolltemp=rolltemp[:nameindex[m]]
                rollKate.append(rolltemp)
              # print(len(rollKate))
              rollKate=np.array(rollKate)
              minroll=np.percentile(rollKate, 30, axis=0)
              maxroll=np.percentile(rollKate, 90, axis=0)
              samplearray=np.concatenate([minroll,maxroll,sampletemp])
              # minroll = np.round(minroll,2)
              # maxroll = np.round(maxroll,2)
              # samplearray = np.round(samplearray,2)
              jsondata[name[m]]={"min":list(minroll),"max":list(maxroll),'sample':list(sampletemp),"range":[(np.min(samplearray)),np.max(samplearray)]}  
          rollfor(name,nameindex,'meas')
          rollfor(name1,nameindex1,'post')    
        # return json.loads(data[0][0]['p1']),200, {'Access-Control-Allow-Origin': '*'}
        return jsondata,200, {'Access-Control-Allow-Origin': '*'}
api.add_resource(Visualization, '/v1.0/model/Visualization/<upid>/<process>/<width>/<length>/<thickness>/<platetype>/')