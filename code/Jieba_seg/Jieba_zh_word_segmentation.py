import re
import jieba
from csv import reader
opened_file = open(r"C:\Users\AERO\Downloads\test_1076.csv", encoding="UTF-8")
read_file = reader(opened_file)
test_1076 = list(read_file)
print(test_1076)

dataset = []
for row in test_1076:
    row = str(row)
    row = re.sub(r'[^\w\s]','',row)
    dataset.append(row)
print(dataset)

seg_data = []
for i in dataset:
    seg_row = jieba.cut(i,cut_all=False)
    seg_join = (" ".join(seg_row))
    seg_data.append(seg_join)
print(seg_data)

import pandas as pd
 
name=['zh_seg']
test=pd.DataFrame(columns=name,data=seg_data)
print(test)
test.to_csv(r"C:\Users\AERO\Downloads\test_seg_v3.csv",encoding='utf-8')