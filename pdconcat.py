import numpy as np
import pandas as pd
import lib.dataprocess as dp
from lib.dataprocess import read_data as rd
path1=r'./target\C2H6O_pusle.csv'
path12=r'./target\HCHO_pusle.csv'
path3 = r'./target\C3H6O_pusle.csv'
df1 =pd.read_csv(path1,index_col=0)
df2 =pd.read_csv(path12,index_col=0)
df3 =pd.read_csv(path3,index_col=0)
concat_list = [df1,df2,df3]
fin=pd.concat(concat_list)
fin.to_csv('./sensor_HCHO_ETH_C3H6O.csv')
