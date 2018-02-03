from analysis.load_posts import load_posts
from analysis.log import log
from analysis._4_classification.standardize_date_format import standardize_date_format
from analysis._5_analyze_source.group_dates import group_dates
from analysis._5_analyze_source.plot_graph import plot_graph
import json


def main(language):
    log(f"Analyzing {language} source", 1)
    all_posts = load_posts(f'analysis/_1_process_raw_data/output/{language}.json')
    standardized = standardize_date_format(all_posts)
    dic = {}
    date_list = []
    for p in standardized:
        source = p['source']
        date = p['date']
        if not source in dic:
            dic[source] = []
        dic[source].append(date)
        date_list.append(date)
    date_list = filter_date(date_list)
    min_date = '20120601'
    max_date = '20180131'

    for source_name in dic:
        dic[source_name] = filter_date(dic[source_name])
        print(source_name)
        print(len(dic[source_name]))
        dic[source_name] = group_dates(min_date, max_date, dic[source_name])

    with open(f'./{language}_source.json', 'w') as outfile:
        print("Saving ", {language})
        json.dump(dic, outfile)


def filter_date(date_list):
    return sorted([x for x in date_list if len(x) == len('YYYYMMDD')])

# main('english')
# main('chinese')
plot_graph('english')
plot_graph('chinese')