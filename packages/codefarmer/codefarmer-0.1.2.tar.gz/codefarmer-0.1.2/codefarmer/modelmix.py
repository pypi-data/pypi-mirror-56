# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:45:37 2019

@author: Qiqi
"""

import pandas as pd
import numpy as np

def modeladd(pro1,pro2,pro3,model1,model2,model3,PRO_PATH,SUB_PATH):   
    
    #用于最终样本的标注
    profile = model1  #只是为了创建一个一样大的
    submitfile = pd.read_csv('submit_example.csv')
    
    print(len(model1))          
    print(len(model2)) 
    print(len(model3)) 
    #进行概率融合     
    for i in range(1,4):
        temp = model1.iloc[:,i]*pro1+model2.iloc[:,i]*pro2+model3.iloc[:,i]*pro3
        profile.iloc[:,i] =temp
        
    #输出概率融合文件
    profile.to_csv(PRO_PATH,index=None)
    
    label = pd.read_csv(PRO_PATH)
    #对概率融合后的结果取最大值输出
    df  = label.iloc[:,1:4]
    df.columns = ['0','1','2']
    result = []
    
    for i in range(0,len(label)):
        s1 = df.iloc[i, :]
        column = list(s1[s1 == s1.max()].index)
        result.append( [int(a) for a in column] )
    
    submitfile.iloc[:,1] = result
    
    #为了防止id顺序不匹配的操作
    submitfile.iloc[:,0] = label.iloc[:,0]
    ####记得改名字！！！！！！！！！！！！！！！！
    submitfile.to_csv(SUB_PATH,index=None)
    return profile,submitfile

def modelaverage(file_path,str_path,outfile_path):   
    promodel = pd.read_csv(file_path)
    
    for i in range(1,5):
        singlemodel = pd.read_csv(str_path.format(i))
        promodel.iloc[:,1:4] = singlemodel.iloc[:,1:4]+promodel.iloc[:,1:4]
    promodel.iloc[:,1:4] = promodel.iloc[:,1:4]/5
    promodel.to_csv(outfile_path,index = None)
    return promodel

