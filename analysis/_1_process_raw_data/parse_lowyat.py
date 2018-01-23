import csv
import pandas
from bs4 import UnicodeDammit
from pprint import pprint
from analysis_process.Post import Post

def parse_lowyat(file_path):
    if("links_retrieved" in file_path):
        return [Post()]
    result = []
    # try:
    result.append(read_title(file_path))
    with open(file_path, 'r', errors='ignore') as csvfile:
        df = pandas.read_csv(csvfile, skiprows=[0])
        for index, row in df.iterrows():
            p = Post()
            p.date = str(row['date'])
            p.value = row['text']
            p.source = 'lowyat'
            if(isinstance(p.value, str)):
                result.append(p)
    return result
    # except:
    #     print("Error at " + file_path)
    # Please comment out try-except, because it will slow down performance

def read_title(file_path):
    file_path = file_path.split('/')[-1]
    if(not 'lowyat' in file_path): 
        return Post()
    p = Post()
    p.date = file_path.split('_')[1]
    p.value = file_path.split('_')[3].split('.')[0]
    p.source = 'lowyat'
    return p
