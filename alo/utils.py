import psycopg2
import re
import json
import pandas as pd

selectlabel='''lmpd.slabid, 
            lmpd.upid,
            lmpd.productcategory, 
            lmpd.steelspec,
            lmpd.toc,
            
            lmpd.tgtplatethickness2,
            lmpd.tgtwidth,
            lmpd.tgtplatelength2,
            lfat.slab_thickness,
            lfat.slab_width,
            lfat.slab_length,
            lfat.slab_weight_act,
            lfat.charging_temp_act,

            lff.ave_temp_entry_pre,
            lff.temp_uniformity_entry_pre,
            lff.sur_temp_entry_pre,
            lff.center_temp_entry_pre,
            lff.skid_temp_entry_pre,
            lff.ave_temp_pre,
            lff.staying_time_pre,
            lff.ave_temp_entry_1,
            lff.temp_uniformity_entry_1,
            lff.sur_temp_entry_1,
            lff.center_temp_entry_1,
            lff.skid_temp_entry_1,
            lff.ave_temp_1,
            lff.staying_time_1,
            lff.ave_temp_entry_2,
            lff.temp_uniformity_entry_2,
            lff.sur_temp_entry_2,
            lff.center_temp_entry_2,
            lff.skid_temp_entry_2,
            lff.ave_temp_2,
            lff.staying_time_2,
            lff.ave_temp_entry_soak,
            lff.temp_uniformity_entry_soak,
            lff.sur_temp_entry_soak,
            lff.center_temp_entry_soak,
            lff.skid_temp_entry_soak,
            lff.ave_temp_soak,
            lff.staying_time_soak,
            lff.ave_temp_dis,
            lff.temp_uniformity_dis,
            lff.sur_temp_dis,
            lff.center_temp_dis,
            lff.skid_temp_dis,
            lfat.t_0,
            lfat.t_1,
            lfat.t_2,
            lfat.t_3,
            lfat.t_4,
            lfat.t_5,
            lfat.t_6,
            --lfat.meas_temp_0,
            --lfat.meas_temp_1,
            --lfat.meas_temp_2,
            --lfat.meas_temp_3,
            --lfat.meas_temp_4,
            --lfat.meas_temp_5,
            --lfat.meas_temp_6,
            --lfat.meas_temp_7,
            --lfat.meas_temp_8,
            --lfat.meas_temp_9,
            --lfat.meas_temp_10,
            --lfat.meas_temp_11,
            --lfat.meas_temp_12,
            --lfat.meas_temp_13,
            --lfat.meas_temp_14,
            --lfat.meas_temp_15,
            --lfat.meas_temp_16,
            --lfat.meas_temp_17,
            --lfat.meas_temp_18,
            --lfat.meas_temp_19,

            lmp.topwrplatecountfm,
            lmp.topwrplatecountrm,
            lmp.topbrplatecountfm,
            lmp.topbrplatecountrm,
            lmp.botbrplatecountfm,
            lmp.botbrplatecountrm,
            lmp.botwrplatecountfm,
            lmp.botwrplatecountrm,
            lmp.crownbody,
            lmp.crowntotal,
            lmp.devcrownbody,
            lmp.devcrowntotal,
            lmp.devthicknesscentertotal,
            lmp.devthicknessclosetotal,
            lmp.devwedgebody,
            lmp.devwedgetotal,
            lmp.maxcrownbody,
            lmp.maxcrowntotal,
            lmp.maxthicknesscentertotal,
            lmp.maxthicknessclosetotal,
            lmp.maxwedgebody,
            lmp.maxwedgetotal,
            lmp.mincrownbody,
            lmp.mincrowntotal,
            --lmp.minthicknesscenterbody,
            --lmp.minthicknesscenterhead,
            lmp.minthicknesscentertotal,
            lmp.minthicknessclosebody,
            lmp.minthicknessclosehead,
            lmp.minthicknessclosetotal,
            --lmp.minwedgebody,
            --lmp.minwedgehead,
            --lmp.minwedgetail,
            lmp.minwedgetotal,
            lmp.ratiolpls,
            lmp.thicknesscenterbody,
            lmp.thicknesscenterhead,
            lmp.thicknesscentertotal,
            lmp.thicknessclosebody,
            lmp.thicknessclosehead,
            lmp.thicknessclosetotal,
            lmp.wedgebody,
            lmp.wedgetotal,

            lcp.avg_p1,
            lcp.std_p1,
            lcp.max_p1,
            lcp.min_p1,
            lcp.avg_p2,
            lcp.std_p2,
            lcp.max_p2,
            lcp.min_p2,
            lcp.avg_sct,
            lcp.std_sct,
            lcp.max_sct,
            lcp.min_sct,
            lcp.avg_fct,
            lcp.std_fct,
            lcp.max_fct,
            lcp.min_fct,
            lcp.avg_p5,
            lcp.std_p5,
            lcp.max_p5,
            lcp.min_p5,
            lcp.avg_cr_cal,
            lcp.std_cr_cal,
            lcp.max_cr_cal,
            lcp.min_cr_cal,
            lcp.avg_cr_act,
            lcp.std_cr_act,
            lcp.max_cr_act,
            lcp.min_cr_act,
            lcp.avg_time_b,
            lcp.std_time_b,
            lcp.max_time_b,
            lcp.min_time_b,
            lcp.avg_time_w,
            lcp.std_time_w,
            lcp.max_time_w,
            lcp.min_time_w,
            lcp.avg_time_a,
            lcp.std_time_a,
            lcp.max_time_a,
            lcp.min_time_a,
            lcp.speed_ratio,
            --lcp.last_cooling_zone_length,
            lcp.last_water_temp,
            lcp.last_air_temp'''
# selection=[]
# ismissing={'all_processes_statistics_ismissing':True,'cool_ismissing':True,'fu_temperature_ismissing':True,'m_ismissing':True,'fqc_ismissing':True}   
# tgtwidthSelect=['2.895','4.48']
# tgtlengthSelect=['16.137','40.382']
# tgtthicknessSelect=['0.0102','0.0232']
# tocSelect=['2018-12-01 01:41:43','2018-12-10 12:11:43']
# UpidSelect=['18C01025000','18C01032000'];
# Platetypes=['KA36-TM','AB/A'];
# AscOption='toc'
# Limition='100';
def readConfig():
    # f = open('usr/src/config/config.txt')
    # f = open('usr/src/app/config.txt')
    f = open('config.txt')
    for line in f:
        configArr = line.split(' ')
        break
    return configArr

def SQLselect(selection,ismissing,tgtwidthSelect,tgtlengthSelect,tgtthicknessSelect,tocSelect,UpidSelect,Platetypes,AscOption,Limition):
    index=0;
    Process=['all_processes_statistics','v1','v2','v3','fqc_label']
    miss=['0','0','0','0','0','0']
    missselect='';
    for i in ismissing:
        if(ismissing[i]):
            # selection.append(Process[index])
            missselect+= ' and '+i+'= '+miss[index];
        index+=1;
#         print(missselect)

    if(len(selection)==0): #select
        select='*'
        print('fjdksjfskdjl')
    else:
        select = ','.join(selection)
#             print(select)
    if(len(tgtwidthSelect)==0):   #tgtwidth
        tgtwidth='';
    else: 
        tgtwidth=' and tgtwidth between '+tgtwidthSelect[0]+' and '+tgtwidthSelect[1]+' '
    if(len(tgtlengthSelect)==0):   #tgtlength
        tgtlength='';
    else: 
        tgtlength=' and tgtlength between '+tgtlengthSelect[0]+' and '+tgtlengthSelect[1]+' '
    if(len(tgtthicknessSelect)==0):  #tgtthickness
        tgtthickness='';
    else: 
        tgtthickness=' and tgtthickness between '+tgtthicknessSelect[0]+' and '+tgtthicknessSelect[1]+' '
    if(len(tocSelect)==0):   #toc
        toc='';
    else: 
        toc=' and toc between '+repr(tocSelect[0])+' and '+repr(tocSelect[1])+' '

    if(len(UpidSelect)==0): #upid
        upid='';
    else: 
        upid=' and (';
        for i in UpidSelect:
            upid+="upid="+repr(i)+' or '
        upid=upid[:-3]
        upid+=')';      
    if(len(Platetypes)==0):  #platetype
        platetype='';
    else: 
        platetype='and (';
        for i in Platetypes:
            platetype+='platetype='+repr(i)+' or '
        platetype=platetype[:-3]
        platetype+=')';
    if(AscOption==''):  #ASC
        ASC='';
    else:
        ASC=' ORDER BY '+AscOption+' DESC';
    if(Limition==''):  #Limit
        Limit='';
    else:
        Limit=' LIMIT '+Limition;
    Query=[tgtwidth,tgtlength,tgtthickness,toc,upid,platetype,missselect]
    index;
    for i in range(len(Query)):
        if(len(Query[i])!=0):
            Query[i]=Query[i][4:]
            # print(Query[i])
            SQL="select "+select+" from dcenter.dump_data " +"where"
            for j in Query:
                SQL+=j;
            SQL+=ASC+Limit;
            print(SQL)
            return SQL
    return "select "+select+" from dcenter.dump_data "+ASC+Limit;

def getData(selection,ismissing,tgtwidthSelect,tgtlengthSelect,tgtthicknessSelect,tocSelect,UpidSelect,Platetypes,AscOption,Limition): 

    #  for docker outside config

    # configArr = readConfig() 
    # conn = psycopg2.connect(database=configArr[0], user=configArr[1], password=configArr[2], host=configArr[3],port=configArr[4])

    SQL=SQLselect(selection,ismissing,tgtwidthSelect,tgtlengthSelect,tgtthicknessSelect,tocSelect,UpidSelect,Platetypes,AscOption,Limition)

    # conn = psycopg2.connect(database='BSData20190713', user='postgres', password='616616', host='219.216.80.18',port='5432')
    conn = psycopg2.connect(database='bg', user='postgres', password='woshimima', host='202.118.21.236',port='5432')

    cursor = conn.cursor()
    cursor.execute(SQL)
    rows = cursor.fetchall()
    
    conn.close()
    return rows
def SQLplateselect(selection,ismissing,tgtwidthSelect,tgtlengthSelect,tgtthicknessSelect,tocSelect,UpidSelect,Platetypes,AscOption,Limition):
    index=0;
    Process=['d.all_processes_statistics','d.v1','d.v2','d.v3','d.fqc_label']
    miss=['0','0','0','0','0','0']
    missselect='';
    for i in ismissing:
        if(ismissing[i]):
            # selection.append(Process[index])
            missselect+= ' and '+i+'= '+miss[index];
        index+=1;
    if(len(selection)==0): #select
        select='*'
        print('fjdksjfskdjl')
    else:
        select = ','.join(selection)
    if(len(tgtwidthSelect)==0):   #tgtwidth
        tgtwidth='';
    else: 
        tgtwidth=' and d.tgtwidth between '+tgtwidthSelect[0]+' and '+tgtwidthSelect[1]+' '
    if(len(tgtlengthSelect)==0):   #tgtlength
        tgtlength='';
    else: 
        tgtlength=' and d.tgtlength between '+tgtlengthSelect[0]+' and '+tgtlengthSelect[1]+' '
    if(len(tgtthicknessSelect)==0):  #tgtthickness
        tgtthickness='';
    else: 
        tgtthickness=' and d.tgtthickness between '+tgtthicknessSelect[0]+' and '+tgtthicknessSelect[1]+' '
    if(len(tocSelect)==0):   #toc
        toc='';
    else: 
        toc=' and d.toc between '+repr(tocSelect[0])+' and '+repr(tocSelect[1])+' '
    if(len(UpidSelect)==0): #upid
        upid='';
    else: 
        upid=' and (';
        for i in UpidSelect:
            upid+="d.upid="+repr(i)+' or '
        upid=upid[:-3]
        upid+=')';      
    if(len(Platetypes)==0):  #platetype
        platetype='';
    else: 
        platetype='and (';
        for i in Platetypes:
            platetype+='m.productcategory='+repr(i)+' or '
        platetype=platetype[:-3]
        platetype+=')';
    if(AscOption==''):  #ASC
        ASC='';
    else:
        ASC=' ORDER BY d.'+AscOption+' DESC';
    if(Limition==''):  #Limit
        Limit='';
    else:
        Limit=' LIMIT '+Limition;
    Query=[tgtwidth,tgtlength,tgtthickness,toc,upid,platetype,missselect]
    index;
    for i in range(len(Query)):
        if(len(Query[i])!=0):
            Query[i]=Query[i][4:]
            # print(Query[i])
            SQL="select "+select+" from dcenter.dump_data d inner  join dcenter.l2_m_primary_data m ON d.upid=m.upid " +"where"
            for j in Query:
                SQL+=j;
            SQL+=ASC+Limit;
            print(SQL)
            return getSQLData(SQL)
    return "select "+select+" from dcenter.dump_data "+ASC+Limit;
def getSQLData(SQLquery): 

    #  for docker outside config

    # configArr = readConfig() 
    # conn = psycopg2.connect(database=configArr[0], user=configArr[1], password=configArr[2], host=configArr[3],port=configArr[4])

    # conn = psycopg2.connect(database='BSData20190713', user='postgres', password='616616', host='219.216.80.18',port='5432')
    conn = psycopg2.connect(database='bg', user='postgres', password='woshimima', host='202.118.21.236',port='5432')

    cursor = conn.cursor()
    cursor.execute(SQLquery)
    rows = cursor.fetchall()
    
    conn.close()
    return rows
def getLabelData(SQLquery): 

    # conn = psycopg2.connect(database='BSData20190713', user='postgres', password='616616', host='219.216.80.18',port='5432')
    conn = psycopg2.connect(database='bg', user='postgres', password='woshimima', host='202.118.21.236',port='5432')

    cursor = conn.cursor()
    cursor.execute(SQLquery)
    rows = cursor.fetchall()
    # print(SQLquery)
    # Extract the column names
    col_names = []
    for elt in cursor.description:
        col_names.append(elt[0])

    conn.close()
    return rows,col_names
def SQLLabel(selection,ismissing,tgtwidthSelect,tgtlengthSelect,tgtthicknessSelect,tocSelect,UpidSelect,Platetypes,AscOption,Limition):

    # index=0,
    Process=['dd.all_processes_statistics','dd.v1','dd.v2','dd.v3','dd.fqc_label']
    miss=['0','0','0','0','0','0']
    missselect='';
    for i in ismissing:
        if(ismissing[i]=='0'):
            missselect+= ' and '+i+'= '+'0';
        # index+=1;
    select=selectlabel
    if(len(selection)==0): #select
        select
    else:
        select =select+ ','+','.join(selection)
    if(len(tgtwidthSelect)==0):   #tgtwidth
        tgtwidth='';
    else: 
        tgtwidth=' and dd.tgtwidth between '+tgtwidthSelect[0]+' and '+tgtwidthSelect[1]+' '
    if(len(tgtlengthSelect)==0):   #tgtlength
        tgtlength='';
    else: 
        tgtlength=' and dd.tgtlength between '+tgtlengthSelect[0]+' and '+tgtlengthSelect[1]+' '
    if(len(tgtthicknessSelect)==0):  #tgtthickness
        tgtthickness='';
    else: 
        tgtthickness=' and dd.tgtthickness between '+tgtthicknessSelect[0]+' and '+tgtthicknessSelect[1]+' '
    if(len(tocSelect)==0):   #toc
        toc='';
    else: 
        toc=' and dd.toc between '+repr(tocSelect[0])+' and '+repr(tocSelect[1])+' '

    if(len(UpidSelect)==0): #upid
        upid='';
    else: 
        upid=' and (';
        for i in UpidSelect:
            upid+="dd.upid="+repr(i)+' or '
        upid=upid[:-3]
        upid+=')';      
    if(len(Platetypes)==0):  #platetype
        platetype='';
    else: 
        platetype='and (';
        for i in Platetypes:
            platetype+='lmpd.productcategory='+repr(i)+' or '
        platetype=platetype[:-3]
        platetype+=')';
    if(AscOption==''):  #ASC
        ASC='';
    else:
        ASC=' ORDER BY dd.'+AscOption+' ASC';
    if(Limition==''):  #Limit
        Limit='';
    else:
        Limit=' LIMIT '+Limition;
    Query=[tgtwidth,tgtlength,tgtthickness,toc,upid,platetype,missselect]
    for i in range(len(Query)):
        if(len(Query[i])!=0):
            Query[i]=Query[i][4:]
            # print(Query[i])
            SQL="select "+select+''' from  dcenter.l2_cc_postcalc lcp
                left join dcenter.l2_fu_flftr60 lff on lcp.slab_no = lff.slab_no
                left join dcenter.l2_fu_acc_t lfat on lcp.slab_no = lfat.slab_no
                left join dcenter.l2_m_primary_data lmpd on lcp.slab_no = lmpd.slabid
                left join dcenter.l2_m_plate lmp on lcp.slab_no = lmp.slabid
                left join dcenter.dump_data dd on dd.upid = lmp.upid where'''
            for j in Query:
                SQL+=j;
            SQL+=ASC+Limit;
            # print(SQL)
            return getLabelData(SQL)
    return "select "+select+" from dcenter.dump_data "+ASC+Limit;

def getFlagArr(str):
    arr = []
    midStr = re.findall('\[[0, 1].*[0,1]\]', str)
    m = re.search('([01]).*([01]).*([01]).*([01]).*([01])', midStr[0])
    for i in range(5):
        arr.append(int(m.group(i+1)))
    # print(arr)
    return arr
def unidimensional_monitoring(upid, data, quantile_num,col_names):

    ##根据upid查询该钢板近一年的同类型数据
    data = data #这里省略，调用封装好的同类型钢板查询接口即可
    data_columns = data.columns.values
    ## 获取同一规格钢板的取过程数据
    process_data = data[col_names[13:134]]
    ## 计算原始过程数据的上下分为点
    lower_limit  = process_data.quantile(q = quantile_num, axis = 0).values
    upper_limit  = process_data.quantile(q = 1-quantile_num, axis = 0).values
    ## 查询此钢板的过程数据（若前端在点击马雷图或散点图前已经储存该数据，则此步骤可以省略）
    upid_data = data[data.upid == upid][col_names[13:134]].values[0]
    
    ## 对同一规格钢板过程数据进行归一化计算
    norm_process_data = (process_data - process_data.min()) / (process_data.max() - process_data.min())
    ## 计算归一化后过程数据的上下分为点
    lower_limit_norm = norm_process_data.quantile(q = quantile_num, axis = 0).values
    upper_limit_norm = norm_process_data.quantile(q = 1-quantile_num, axis = 0).values
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
            'original_value':upid_data[i],
            'original_l':lower_limit[i],
            'original_u':upper_limit[i],
        })
    return result
def data_filter(data,col_names):
    data =  pd.DataFrame(data = data, columns = col_names).dropna(axis=0,how='any').reset_index(drop = True)
    raw_process_data = data[col_names[5:134]]
    data = data[((raw_process_data < 1e+10) & (raw_process_data > -1e+10)).sum(axis=1) == raw_process_data.shape[1]].reset_index(drop = True)
    processdata=data.iloc[:,5:134].values
    return data,processdata
ref = 5