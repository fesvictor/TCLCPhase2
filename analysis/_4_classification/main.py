from analysis._4_classification.standardize_date_format import standardize_date_format
import json
from analysis._4_classification.extract_data import extract_data
from analysis.load_posts import load_posts
from analysis.log import log
from analysis.save_posts import save_posts

START_DATE = '20170101'
END_DATE = '20170108'
def main(language):
    log(f"Standardizing date format of each {language} posts", 0)
    input_dir = f'analysis/_3_label_semantic/{language}.json'
    all_posts = load_posts(input_dir)
    standardized = standardize_date_format(all_posts)
    log(f"Sorting post based on date", 1)
    sorted_posts = sorted(standardized, key=lambda x: x['date'])
    extracted = extract_data(sorted_posts, START_DATE, END_DATE, language )
    log(f'Storing results to analysis/results/{language}_extracted.json', 1)
    json.dump(extracted, open(f'analysis/results/{language}_extracted.json', 'w'))

def get_date_format_of_each_sources(all_posts):
    dic = {}
    for post in all_posts:
        if(post['source'] not in dic):
            dic[post['source']] = post['date']
    import pprint
    pprint.pprint(dic)

main('english')
main('chinese')
