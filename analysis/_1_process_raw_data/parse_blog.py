import csv
from bs4 import UnicodeDammit
from pprint import pprint
from analysis_process.Post import Post

def parse_blog(file_path):
    result = []
    with open(file_path, 'r', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['column1']
            for key, value in row.items():
                if(key in ['column1', 'column2'] or value == ''):
                    continue
                p = Post()
                p.date = date
                p.value = str.lower(value)
                p.source = 'blog'
                result.append(p)
    return result
