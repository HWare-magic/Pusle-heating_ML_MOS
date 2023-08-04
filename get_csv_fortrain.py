# from lib import dataprocess as dp
import numpy as np
import pandas as pd
import os
import lib.dataprocess as dp
from lib.dataprocess import read_data as rd
path1 = './march'
path2 = r''
path_list = [path1]
target_path = './0304'

if not os.path.exists(target_path):
    os.makedirs(target_path)
###
# a=rd(path=path)
# b=a.col_process(col_num=4,cycle_point=6000,concentration=10)
# c=a.col_process(col_num=5,cycle_point=6000,concentration=10)
# # print('b.head=',b.head(5))
# # print('c.head=',c.head(5))
# d =dp.low_sample_rate(ddf=b,div_rate=10)
# print(d.shape)
# print(d.head(5))
###

# a= rd(path=path1)
# file_list = a.file_fold(extension='csv')
# print(file_list)
####  df_dict = {key=filename,value= csv file}
df_dict={}
for i in path_list:
    a=rd(path=i)
    file_name=a.file_fold(extension='csv')
    df_dict.update(file_name)
### for new file change  key_list and HCHO10ppm = eth_dict.get(key_list[i])
HCHO_dict ={k:v for k,v in df_dict.items() if 'HCHO' in k}
eth_dict = {k:v for k,v in df_dict.items() if 'eth' in k}
C3H6O_dict = {k:v for k,v in df_dict.items() if 'C3H6O' in k}
# CO_dict = {k:v for k,v in df_dict.items() if 'CO' in k}

key_list = list(HCHO_dict.keys())
print(key_list)
cat_list=[]
for i in range (len(key_list)):
    HCHO10ppm = HCHO_dict.get(key_list[i])
    conc= (i+1)*10
    df_origin_length =dp.pulse_align(dataframe=HCHO10ppm,cycle_point=6000,col_num=1,low_voltage=1.1,high_volt=2.8,target_length=5800,pre_num=900,concentration=conc)
    # df_origin_length = dp.col_process(dataframe=HCHO10ppm,col_num=4,cycle_point=6000,concentration=conc)
    ddl=df_origin_length.iloc[int(np.floor(len(df_origin_length)/10)):-1]
    low_sample_rate = dp.low_sample_rate(ddl,div_rate=10)
    cat_list.append(low_sample_rate)

df=pd.concat(cat_list)
df.to_csv(target_path+'/HCHO.csv')
