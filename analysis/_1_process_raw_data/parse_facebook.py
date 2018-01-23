import csv
from analysis_process.Post import Post

def parse_facebook(file_path):
    result = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Post()
            p.date = row['status_published']
            p.value = str.lower(row['status_message'] + row['link_name'])
            p.source = 'facebook'
            result.append(p)
    return result
