# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 14:23:55 2018

@author: hpf
"""

import pandas as pd 
import shelve

df_position=pd.read_excel("ASA_position.xlsx",dtype=str)

df_info=pd.read_excel("ASA_clinvar.xlsx",dtype=str)
#df_info=pd.read_csv("2.CSV",sep=",")

df_info_columns=df_info.columns

ref_list=[]


for j in range(len(df_position)):
    name_1=df_position.iloc[j]["Chr"]+"_"+df_position.iloc[j]["MapInfo"]
    ref_list.append(name_1)

shelfile=shelve.open("mydata")
shelfile['ref_list']=ref_list
shelfile.close()


#用于整理表格
def clear_excel(df):
    for i in range(len(df)):
        temp=df.iloc[i]["GRCh37Chromosome"]
        if temp=="|":
            pass
        elif "|" in temp:
            if temp.startswith("|"):
                temp_1=temp.split("|")[1]
            else:
                temp_1=temp.split("|")[0]
            df.at[i,"GRCh37Chromosome"]=temp_1
    
    for j in  range(len(df)):
        temp_2=df.iloc[j]["GRCh37Location"]
        if "-" in temp_2:
            temp_3=temp_2.split("-")
            temp_list=[i.strip() for i in temp_3]
            temp_4=temp_list[0]
            df.at[j,"GRCh37Location"]=temp_4
    return df
                



df_info1=clear_excel(df_info)


#从已经保存的list文件中读入list
#shelfile=shelve.open("mydata")
#ref_list=list(shelfile['cats'])

result_df=pd.DataFrame()
for i in range(len(df_info1)):
    temp1=df_info.iloc[i]["GRCh37Chromosome"]
    temp2=df_info.iloc[i]["GRCh37Location"]
    if temp1.isalnum() and temp2.isalnum():
        if temp1=='nan' or temp2=='nan':
            pass
        else:
            temp=temp1+"_"+temp2
            if temp in ref_list:
                result_df=result_df.append(df_info.iloc[i])
   
 
result_df[df_info_columns].to_csv("ASA_result.csv",header=True,index=False)













       
'''

for j in range(len(df_position)):
    name_1=str(int(df_position.iloc[j]["Chr"]))+"_"+str(int(df_position.iloc[j]["MapInfo"]))
    ref_list.append(name_1)

def split_str(a):
    if isinstance(a,basestring):
        if "|" in a:
            b=a.split("|")[0]
            if b=="" :
                b=a.split("|")[1]
                if b=="":
                    return False
                else:
                    return b
            return b   
        else:
           return a
    else:
        return str(int(a))
            
result_df=pd.DataFrame()

for i in range(len(df_info)):
    temp=df_info.iloc[i]["GRCh37Chromosome"]
    if not(isinstance(temp,basestring)):
        if np.isnan(temp):
            continue
        
    elif split_str(temp) and not(isinstance(df_info.iloc[i]["GRCh37Location"],basestring)):
        name=split_str(temp)+"_"+str(int(df_info.iloc[i]["GRCh37Location"]))
        if name in ref_list:
            result_df=result_df.append(df_info.iloc[i])
    else:
        pass




#    else:
#        name=str(int(df_info.iloc[i]["GRCh37Chromosome"]))+"_"+str(int(df_info.iloc[i]["GRCh37Location"]))
#        if name in ref_list:
#            result_df=result_df.append(df_info.iloc[i])

result_df.to_csv("ASA_result.csv",header=True,index=False)
'''



