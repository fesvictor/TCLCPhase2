import pandas
from bs4 import UnicodeDammit
from analysis_process.Post import Post

def parse_twitter(file_path):
    with open(file_path, 'r', errors='ignore') as file:
        first_line = file.readline()
        if '< HEAD' not in first_line:
            file.seek(0) # This to make sure the file pointer go backs to the first line
        result = []
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            p = Post()
            p.date = str(row['created_at'])
            p.value = row['text']
            p.source = 'twitter'
            if(isinstance(p.value, str)):
                result.append(p)
    return result
