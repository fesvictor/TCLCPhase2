import csv
from analysis.libs.Post import Post

def parse_facebook_csv(file_path):
    result = []
    if not file_path.endswith('.csv'):
        return result
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Post()
            p.origin = file_path
            p.date = row['status_published']
            p.value = str.lower(row['status_message'] + row['link_name'])
            p.source = 'facebook'
            result.append(p)
    return result
