from analysis.libs.Post import Post
from bs4 import UnicodeDammit
from hanziconv import HanziConv
from pprint import pprint
import csv
import pandas

def parse_carinet(file_path):
    result = []
    result.append(read_title(file_path))
    with open(file_path, 'r', errors='ignore') as csvfile:
        df = pandas.read_csv(csvfile, skiprows=[0], error_bad_lines=False)
        for index, row in df.iterrows():
            p = Post()
            p.origin = file_path
            p.date = str(row['date'])
            if(type(row['text']) is not str): 
                continue
            p.value = HanziConv.toSimplified(row['text'].replace("\n", "").strip())
            p.source = 'carinet'
            if(isinstance(p.value, str)):
                result.append(p)
    return result

def read_title(file_path):
    file_path = file_path.split('/')[-1]
    if(not 'carinet' in file_path): 
        return Post()
    p = Post()
    p.date = file_path.split('_')[1]
    p.value = file_path.split('_')[2].split('.')[0]
    p.origin = file_path
    p.source = 'carinet'
    return p

