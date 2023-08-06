# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:58:17 2019

@author: Qiqi
"""

import pandas as pd 
import numpy as np
from codefarmer import modelmix
def main_add(str_path1,str_path2,str_path3,str_path4,PRO_PATH,SUB_PATH):
   
    bert = modelmix.modelaverage(str_path1,'pro_bert.csv')
    xlnet = modelmix.modelaverage(str_path2,'pro_xlnet.csv')
    large_bert = modelmix.modelaverage(str_path3,'pro_largebert.csv')
    roberta = modelmix.modelaverage(str_path4,'pro_roberta.csv')
    

    large_bert85_bert85_roberta15,sub_lbr= modelmix.modeladd(
                                    0.85,0.85,0.15,large_bert,bert,roberta,
                                    'pro_large_bert85_bert85_roberta15.csv',
                                    'submit_large_bert85_bert85_roberta15.csv')
    

    roberta9_xlnet9_bert1,sub_rxb = modelmix.modeladd(0.9,0.9,0.1,roberta,xlnet,bert,
                                              'pro_roberta9_xlnet9_bert1.csv',
                                              'submit_roberta9_xlnet9_bert1.csv')
    

    submodel1,subsubmit1 = modelmix.modeladd(0.5,0.5,0,large_bert85_bert85_roberta15,roberta9_xlnet9_bert1,
                                  bert,'pro_submodel1.csv',
                                        'submit_submodel1.csv')
    

    large_bert8_bert1_roberta1,sub_lbbr = modelmix.modeladd(0.8,0.1,0.1,large_bert,bert,roberta,
                                                   'pro_large_bert8_bert1_roberta1.csv',
                                                   'submit_large_bert8_bert1_roberta1.csv')

    submodel2,subsubmit2 = modelmix.modeladd(0.6,0.4,0,large_bert8_bert1_roberta1,
                                         large_bert85_bert85_roberta15,bert,
                                'pro_submodel2.csv','submit_submodel2.csv')
    

    model_3,submit3 = modelmix.modeladd(0.9,0.1,0,submodel2,submodel1,bert,
                                'pro_model_3.csv','submit_model_3.csv')

    model_4,submit4 = modelmix.modeladd(0.5,0.5,0,large_bert8_bert1_roberta1, 
                                          large_bert85_bert85_roberta15,bert,
                                           'pro_model_4.csv','submit_model_4.csv')
    #生成结果文件
    for i in [1,2,3,4]:
        modelmix.Pro_to_submit(str_path3.format(i),('submit_large{}.csv'.format(i)) )

    submitmodel_1,promodel_1 = modelmix.vote_prob('submit_large{}'.format(1),
            'submit_large{}'.format(2),'submit_large{}'.format(3),
            'submit_large{}'.format(4),str_path3.format(1),str_path3.format(2),
            str_path3.format(3),str_path3.format(4),'pro_model_1.csv','submit_model_1.csv')

    model_2,submit2 = modelmix.modeladd(0.85,0.15,0,model_3,promodel_1,bert, 
                               'pro_model_2.csv' ,'submit_model_2.csv')
  
    submitmodel,promodel = modelmix.vote_prob('submit_model_1.csv','submit_model_2.csv',
                    'submit_model_3.csv','submit_model_4.csv','pro_model_1.csv',
                    'pro_model_2.csv', 'pro_model_3.csv', 'pro_model_4.csv',
                    PRO_PATH,SUB_PATH)
	
    return None




 