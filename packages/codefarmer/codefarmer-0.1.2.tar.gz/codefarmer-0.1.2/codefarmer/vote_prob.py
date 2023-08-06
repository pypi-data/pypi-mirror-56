import pandas as pd
import numpy as np
def vote_prob(path1,path2,path3,path4,ave_path1,ave_path2,ave_path3,ave_path4):
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
    
    new.to_csv('./result/vote_xlnet.csv',index = None)
    ave_new.to_csv('./result/prob_vote_xlnet.csv',index = None)
    return new,ave_new
