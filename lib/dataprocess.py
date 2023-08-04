import pandas as pd
import numpy as np
import os
import csv
class MyClass:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(f"My name is {self.name}.")


class read_data:
    def __init__(self,path):
        self.path= path
    def file_fold(self,extension):
        '''
        only for csv now ,  get path by class parameter  return a dict :key is file name value is content
        '''
        files = [file for file in os.listdir(self.path) if file.endswith(extension)]
        file_names_key=[]
        for file_name in files:
            basename = os.path.basename(file_name)
            var_name = os.path.splitext(basename)[0]
            file_names_key.append(var_name) ## get file name for dict.key
        if extension == 'csv':
            file_names_value = [pd.read_csv(os.path.join(self.path, file)) for file in files] # file_name_value is a list for csv content
        else:
            print("extension is not support")
        file_names_dict = dict(zip(file_names_key, file_names_value))
        return file_names_dict

def pulse_align(dataframe,cycle_point,col_num,low_voltage,high_volt,target_length,pre_num,concentration):
    '''
    get a dataframe,cycle_pouint:a cycle include how much point,col_num:process column in dataframe such as 3 is sensor3(vol)
    low_voltage and high  voltage  in order to find pulse rise edge point
    target length : output serise length
    pre_num: output start point how long before pulse point
    concentration :for add concentration label
    return a datafrane with (num_rows,target_length+1) the 1 is label column
    '''
    z=[]
    df = dataframe
    ddf = pd.DataFrame(np.zeros(len(df)))
    col_name = df.columns.values[col_num]
    col_data = df[col_name]
    pulse_data =df.loc[:," pulse "]
    num_rows = int(np.floor(len(col_data) / cycle_point))
    ## find pulse point
    for i in range(num_rows):
        z.append(0)
        for j in range(i*cycle_point,(i+1)*cycle_point):
            if pulse_data[j] < low_voltage and pulse_data[j+1] > high_volt:
                z[i]=pulse_data.index[j]
    print(z)
    ### rearrange the df
    for i,j in enumerate(z):
        for k in range(target_length):
            ddf.iloc[i*target_length+k] = col_data.iloc[j-pre_num+k]
    ddf1=ddf.iloc[0:num_rows*target_length] ## delete other '0' data in ddf
    dff=pd.DataFrame(ddf1.values[:].reshape(num_rows,target_length))
    dff['concentration'] = concentration
    return dff

def col_process(dataframe,col_num,cycle_point,concentration):
    df=dataframe
    #print(df.head(5))
    col_name = df.columns.values[col_num]
    col_data = df[col_name]
    n = cycle_point
    num_rows = int(np.floor(len(col_data) / n))
    num_cols = n
    if num_rows==60:
        new_table = pd.DataFrame(np.zeros((num_rows, num_cols)), columns=[f'Column{i + 1}' for i in range(num_cols)])
        new_table = col_data.values[0:360000].reshape(num_rows, num_cols)
        ddf = pd.DataFrame(new_table)
        ddf['concentration'] = concentration
    else:
        new_table = pd.DataFrame(np.zeros((num_rows, num_cols)), columns=[f'Column{i + 1}' for i in range(num_cols)])
        new_table = col_data.values[0:num_rows*num_cols].reshape(num_rows, num_cols)
        ddf = pd.DataFrame(new_table)
        ddf['concentration'] = concentration
    return ddf


def low_sample_rate(ddf,div_rate):
    new_df = pd.DataFrame()
    # print(ddf.shape[1])
    for i in range(0, ddf.shape[1], div_rate):
        new_df = pd.concat([new_df, ddf.iloc[:, i]], axis=1)
    return new_df

def split_csv_file(input_file, output_prefix, num_files=3):
    # 读取原始CSV文件
    with open(input_file, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # 计算每个文件的行数
    total_rows = len(rows)
    rows_per_file = total_rows // num_files

    # 分割文件并保存
    for i in range(num_files):
        start = i * rows_per_file
        end = start + rows_per_file
        output_file = f'{output_prefix}_{i+1}.csv'
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows[start:end])

        print(f'保存文件: {output_file}')