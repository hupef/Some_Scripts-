# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 10:13:08 2018

@author: hpf
"""

import pandas as pd
import re
import os

#df=pd.read_csv("P21b-P21a.hg19_multianno.csv",dtype=str)

#出列表格，分割列名为name的多个值为单个值多行的情况
def split_gene(df,name):
    df_result=pd.DataFrame()
    for i in range(len(df)):
        temp=df.iloc[i]
        temp_name_list=temp[name].split(",")
        for j in range(len(temp_name_list)):
            df.at[i,name]=temp_name_list[j]
            temp_line=df.iloc[i]
            df_result=df_result.append(temp_line)
    return df_result


df_result1=pd.DataFrame()

for path,dir,file in os.walk("./"):
    for name in file:
        if re.match("(.*)a.hg19_multianno.csv",name):
            temp_name=re.match("(.*)a.hg19_multianno.csv",name).group(1)
            name_a=temp_name+"a.hg19_multianno.csv"
            name_b=temp_name+"b.hg19_multianno.csv"
            df_temp_a=pd.read_csv(name_a,dtype=str)
            df_temp_b=pd.read_csv(name_b,dtype=str)
            
            df_temp_a["sampleID"]=temp_name
            df_temp_b["sampleID"]=temp_name
            
            temp_result=temp_name+".dealed.csv"
            
            temp_columns=['Gene.refGene','sampleID']
            
            df_temp1=split_gene(df_temp_a,"Gene.refGene")
            df_temp2=split_gene(df_temp_b,"Gene.refGene")
            
            
            df_temp1a=df_temp1[temp_columns].drop_duplicates() #去重，对于单个样本中只会出现单个基因名
            df_temp2b=df_temp2[temp_columns].drop_duplicates()
            
            df_temp1a= df_temp1a.append(df_temp2b,ignore_index=True)
            df_temp3=df_temp1a.groupby("Gene.refGene")["sampleID"].count()
            df_temp4=df_temp3.reset_index()
            df_temp5=df_temp4[df_temp4["sampleID"]>1]
            #上一列 >1 就表示交集的部分。
            
            df_temp5["sampleID1"]=temp_name
            df_temp6=df_temp5[['Gene.refGene','sampleID1']]
           

            df_temp6.to_csv(temp_name,header=True,index=False)
            print temp_name
            df_result1=df_result1.append(df_temp6,ignore_index=True)
 

df_result1.to_csv("all_gene_samples.txt",header=True,index=False)

df_result2=df_result1.groupby("Gene.refGene")["sampleID1"].count().reset_index()

df_result3=df_result2.sort_values(by=["sampleID1"],ascending=False)
df_result3.to_csv("all_gene_samples_sort.txt",header=True,index=False)
          
            
            
            














'''
#用来输出分割Gene.refGene列中多个基因名的问题

for path,dir,file in os.walk("./"):
    for name in file:
        if re.match("(.*).hg19_multianno.csv",name):
            temp_name=re.match("(.*).hg19_multianno.csv",name).group(1)
            df_temp=pd.read_csv(name,dtype=str)
            df_temp["sampleID"]=temp_name
            temp_result=temp_name+".dealed.csv"
            temp_columns=['Chr','Start','End','Ref','Alt','Gene.refGene','sampleID']
            df_temp1=split_gene(df_temp,"Gene.refGene")
            df_temp1[temp_columns].to_csv(temp_result,header=True,index=False)
'''           

          
