# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:58:17 2019

@author: Qiqi
"""

import pandas as pd 
import numpy as np
import modelmix 
def main_add():
    PATH1 = './1121_result/model_bert_wwm_ext0/sub.csv'
    str_path1 = './1121_result/model_bert_wwm_ext{}/sub.csv'
    out_path1 = './1121_result/aver_pro_bert.csv'
    
    PATH2 = './1121_result/model_xlnet0/sub.csv'
    str_path2 = './1121_result/model_xlnet{}/sub.csv'
    out_path2 = './1121_result/aver_pro_xlnet.csv'
    
    PATH3 = './1121_result/model_large_bert_wwm_ext0/sub.csv'
    str_path3 = './1121_result/model_large_bert_wwm_ext{}/sub.csv'
    out_path3 = './1121_result/aver_pro_large_bert.csv'
    
    PATH4 = './1121_result/model_roberta0/sub.csv'
    str_path4 = './1121_result/model_roberta{}/sub.csv'
    out_path4 = './1121_result/aver_pro_roberta.csv'
    
    bert = modelmix.modelaverage(PATH1,str_path1,out_path1)
    xlnet = modelmix.modelaverage(PATH2,str_path2,out_path2)
    large_bert = modelmix.modelaverage(PATH3,str_path3,out_path3)
    roberta = modelmix.modelaverage(PATH4,str_path4,out_path4)
    
    #0.81171a
    large_bert85_bert85_roberta15 = modelmix.modeladd(0.85,0.85,0.15,large_bert,bert,roberta,
                                    'pro_large_bert85_bert85_roberta15.csv',
                                    'submit_large_bert85_bert85_roberta15.csv')
    
    #0.81171b
    roberta9_xlnet9_bert1 = modelmix.modeladd(0.9,0.9,0.1,roberta,xlnet,bert,
                                              'pro_roberta9_xlnet9_bert1.csv',
                                              'submit_roberta9_xlnet9_bert1.csv')
    
    #0.81336
    submodel1 = modelmix.modeladd(0.5,0.5,0,large_bert85_bert85_roberta15,roberta9_xlnet9_bert1,
                                  bert,'pro_submodel1.csv',
                                        'submit_submodel1.csv')
    
    #0.81204
    large_bert8_bert1_roberta1 = modelmix.modeladd(0.8,0.1,0.1,large_bert,bert,roberta,
                                                   'pro_large_bert8_bert1_roberta1.csv',
                                                   'submit_large_bert8_bert1_roberta1.csv')
    #0.81672
    submodel2 = modelmix.modeladd(0.6,0.4,0,large_bert8_bert1_roberta1,
                                         large_bert85_bert85_roberta15,bert,
                                'pro_submodel2.csv','submit_submodel2.csv')
    
    #0.81851
    model_3 = modelmix.modeladd(0.9,0.1,0,submodel2,submodel1,bert,
                                'pro_model_3.csv','submit_model_3.csv')
    #0.8185
    model_4 = modelmix.modeladd(0.5,0.5,0,large_bert8_bert1_roberta1, 
                                          large_bert85_bert85_roberta15,bert,
                                           'pro_model_4.csv','submit_model_4.csv')
    
#    #0.81689
#    model_1 = vote_prob.vote_prob()
#    #0.81956
#    model_2 = modelmix.modeladd(0.85,0.15,0,model_3,model_1,bert, 
#                                'pro_model_2.csv','submit_model_2.csv')
#    
#    model = vote_prob.vote_prob()
    return None




 