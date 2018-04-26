from analysis.libs.load_posts import load_posts
from analysis.libs.log import log
from analysis._4_classification.standardize_date_format import standardize_date_format
from analysis._5_analyze_source.group_dates import group_dates
from analysis._5_analyze_source.plot_graph import plot_graph
import json

MIN_DATE = '20180101' 
MAX_DATE = '20180430'


def main(language):
    log(f"Analyzing {language} source", 1)
    dir1 = '_1_process_raw_data/output' # use dir1 to analyze raw source
    dir2 = '_2_remove_unrelated_data' # use dir2 to analyze filtered source
    all_posts = load_posts(
        f'analysis/{dir1}/{language}.json')
    all_posts = [x for x in all_posts if x["date"] != '']
    standardized = standardize_date_format(all_posts)
    dic = {}
    date_list = []
    for p in standardized:
        source = p['source']
        date = p['date']
        if not source in dic:
            dic[source] = []
        if date > MIN_DATE:
            dic[source].append(date)
            date_list.append(date) 
    date_list = filter_date(date_list)

    for source_name in dic:
        dic[source_name] = filter_date(dic[source_name])
        print(source_name)
        print(len(dic[source_name]))
        dic[source_name] = group_dates(MIN_DATE, MAX_DATE, dic[source_name])

    with open(f'analysis/_5_analyze_source/{language}_source.json', 'w') as outfile:
        print("Saving ", {language})
        json.dump(dic, outfile)


def filter_date(date_list):
    return sorted([x for x in date_list if len(x) == len('YYYYMMDD')])


main('english')
plot_graph('english', MIN_DATE, MAX_DATE)
main('chinese')
plot_graph('chinese', MIN_DATE, MAX_DATE)
