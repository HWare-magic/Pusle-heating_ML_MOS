import pandas as pd
import statistics
import numpy as np


DATAPATH = './0304/HCHO.csv' #
file_path = './0304/HCHO_std.csv'
data = pd.read_csv(DATAPATH, index_col=0, header=0)
### str label to classfy
a = data.iloc[:, 0:-2]
b = a.values
condu =  np.empty(580)
std = []
for i in range(b.shape[0]):
    condu1 = b[i] /((5-b[i])*10)
    std1 = statistics.stdev(condu1)
    condu1 = condu1/std1
    std.append(std1)
    condu = np.vstack((condu,condu1))

print(condu.shape[0])
print(std)
df2 =  pd.DataFrame(condu[1:])

df2.insert(loc=580,column='concentration',value=data.iloc[:, 580].values)
df2.insert(loc=581,column='gas type',value=data.iloc[:, 581].values)
df2.to_csv(file_path, index=True, header=True)
#np.savetxt(file_path, condu[1:], delimiter=",")

