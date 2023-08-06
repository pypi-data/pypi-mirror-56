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

def Pro_to_submit(PRO_PATH,SUB_PATH):
    label = pd.read_csv(PRO_PATH)
    submitfile = pd.read_csv('submit_example.csv')
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
    return None

def modelaverage(str_path,outfile_path):   
    promodel = pd.read_csv(str_path.format(1))
    
    for i in range(1,5):
        singlemodel = pd.read_csv(str_path.format(i))
        promodel.iloc[:,1:4] = singlemodel.iloc[:,1:4]+promodel.iloc[:,1:4]
    promodel.iloc[:,1:4] = promodel.iloc[:,1:4]/5
    promodel.to_csv(outfile_path,index = None)
    return promodel

def vote_prob(path1,path2,path3,path4,ave_path1,ave_path2,ave_path3,ave_path4,PRO_PATH,SUB_PATH):
    #读取结果文件
    read1 = pd.read_csv(path1)
    read2 = pd.read_csv(path2)
    read3 = pd.read_csv(path3)
    read4 = pd.read_csv(path4)
    new = pd.read_csv(path1)
    
    #读取带有标签概率值得文件
    ave_read1 = pd.read_csv(ave_path1)
    ave_read2 = pd.read_csv(ave_path2)
    ave_read3 = pd.read_csv(ave_path3)
    ave_read4 = pd.read_csv(ave_path4)
    ave_new = pd.read_csv(ave_path1)
    
    count = 0
    n000 = 0 ; n111 = 0 ; n222 = 0
    n00 = 0 ; n11 = 0 ; n22 = 0
    nn = 0
    
    #对四个文件的结果进行投票，并计算每个标签的投票结果的概率值
    
    for i in range(len(read1)):
    	if read1.iloc[i,1] == read2.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1]:
    		new.iloc[i,1] = read1.iloc[i,1]
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/4
    		count += 1
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == read3.iloc[i,1] == 0):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:])/3
    		n000 += 1
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == read4.iloc[i,1] == 0):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n000 += 1
    	elif (read2.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1] == 0):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n000 += 1
    	elif (read1.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1] == 0):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n000 += 1
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == read3.iloc[i,1] == 1):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:])/3
    		n111 += 1
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == read4.iloc[i,1] == 1):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n111 += 1
    	elif(read2.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1] == 1):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n111 += 1
    	elif (read1.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1] == 1):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n111 += 1
    
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == read3.iloc[i,1] == 2):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:])/3
    		n222 += 1
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == read4.iloc[i,1] == 2):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n222 += 1
    	elif(read2.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1] == 2):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n111 += 1
    	elif (read1.iloc[i,1] == read3.iloc[i,1] == read4.iloc[i,1] == 2):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/3
    		n111 += 1	
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == 0 and read3.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:])/2
    		n00 += 1 
    	elif (read1.iloc[i,1] == read3.iloc[i,1] == 0 and read2.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read3.iloc[i,1:])/2
    		n00 += 1 
    	elif (read1.iloc[i,1] == read4.iloc[i,1] == 0 and read2.iloc[i,1] != read3.iloc[i,1]):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n00 += 1 
    	elif (read2.iloc[i,1] == read3.iloc[i,1] == 0 and read1.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:])/2
    		n00 += 1 
    	elif (read2.iloc[i,1] == read4.iloc[i,1] == 0 and read1.iloc[i,1] != read3.iloc[i,1]):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n00 += 1 
    	elif (read3.iloc[i,1] == read4.iloc[i,1] == 0 and read1.iloc[i,1] != read2.iloc[i,1]):
    		new.iloc[i,1] = 0
    		ave_new.iloc[i,1:] = (ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n00 += 1 		
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == 1 and read3.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:])/2
    		n11 += 1 
    	elif (read1.iloc[i,1] == read3.iloc[i,1] == 1 and read2.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read3.iloc[i,1:])/2
    		n11 += 1 
    	elif (read1.iloc[i,1] == read4.iloc[i,1] == 1 and read2.iloc[i,1] != read3.iloc[i,1]):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n11 += 1 
    	elif (read2.iloc[i,1] == read3.iloc[i,1] == 1 and read1.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:])/2
    		n11 += 1 
    	elif (read2.iloc[i,1] == read4.iloc[i,1] == 1 and read1.iloc[i,1] != read3.iloc[i,1]):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n11 += 1 
    	elif (read3.iloc[i,1] == read4.iloc[i,1] == 1 and read1.iloc[i,1] != read2.iloc[i,1]):
    		new.iloc[i,1] = 1
    		ave_new.iloc[i,1:] = (ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n11 += 1 
    	elif (read1.iloc[i,1] == read2.iloc[i,1] == 2 and read3.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read2.iloc[i,1:])/2
    		n22 += 1 
    	elif (read1.iloc[i,1] == read3.iloc[i,1] == 2 and read2.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read3.iloc[i,1:])/2
    		n22 += 1 
    	elif (read1.iloc[i,1] == read4.iloc[i,1] == 2 and read2.iloc[i,1] != read3.iloc[i,1]):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read1.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n22 += 1 
    	elif (read2.iloc[i,1] == read3.iloc[i,1] == 2 and read1.iloc[i,1] != read4.iloc[i,1]):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read3.iloc[i,1:])/2
    		n22 += 1 
    	elif (read2.iloc[i,1] == read4.iloc[i,1] == 2 and read1.iloc[i,1] != read3.iloc[i,1]):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read2.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n22 += 1 
    	elif (read3.iloc[i,1] == read4.iloc[i,1] == 2  and read1.iloc[i,1] != read2.iloc[i,1]):
    		new.iloc[i,1] = 2
    		ave_new.iloc[i,1:] = (ave_read3.iloc[i,1:] + ave_read4.iloc[i,1:])/2
    		n22 += 1 
    	else:
    		new.iloc[i,1] = read4.iloc[i,1]
    		ave_new.iloc[i,1:] = read4.iloc[i,1:] 
    		nn += 1
    print(count,n000,n111,n222,n00,n11,n22,nn)
    
    new.to_csv(SUB_PATH,index = None)
    ave_new.to_csv(PRO_PATH,index = None)
    return new,ave_new
