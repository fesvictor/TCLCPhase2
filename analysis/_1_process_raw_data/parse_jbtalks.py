import csv
from hanziconv import HanziConv
from analysis_process.Post import Post


def parse_jbtalks(file_name):
    result = []
    result.append(create_post_from(file_name))
    date = result[0].date
    with open(file_name, 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Post()
            p.date = date
            p.value = HanziConv.toSimplified(row['text'].replace("\n", "").strip())
            p.source = 'jbtalks'
            result.append(p)
    return result


def create_post_from(file_path):
    p = Post()
    tokens = file_path.split('/')[-1].split('_')
    p.date = tokens[1]
    p.value = tokens[2].split('.')[0].replace(' ', '')
    p.source = 'jbtalks'
    return p
