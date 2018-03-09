from analysis.libs.AnalysisRunner import AnalysisRunner
from analysis._2_remove_unrelated_data.load_labels import load_labels
from analysis._4_classification.extract_data import extract_data
from analysis._4_classification.get_keywords import get_keywords
from analysis._4_classification.replace_synonyms import replace_synonyms
from analysis._4_classification.standardize_date_format import standardize_date_format
from analysis.libs.load_posts import load_posts
from analysis.libs.log import log
from analysis.libs.save_posts import save_posts
import json

START_DATE = '20170701'
END_DATE = '20171231'


def main(language):
    log(f"Standardizing date format of each {language} posts", 0)
    post_str = str(load_posts(f'analysis/_3_label_semantic/{language}.json'))
    post_str = replace_synonyms(post_str, "../../keywords/target/")
    all_posts = eval(replace_synonyms(post_str,  get_keywords(language)))
    standardized = standardize_date_format(all_posts)
    log(f"Sorting post based on date", 1)
    sorted_posts = sorted(standardized, key=lambda x: x['date'])
    extracted = extract_data(sorted_posts, START_DATE, END_DATE, language)
    log(f'Storing results to analysis/results/{language}_extracted.json', 1)
    json.dump(extracted, open(
        f'analysis/results/{language}_extracted.json', 'w'), ensure_ascii=False)


def get_date_format_of_each_sources(all_posts):
    dic = {}
    for post in all_posts:
        if(post['source'] not in dic):
            dic[post['source']] = post['date']
    import pprint
    pprint.pprint(dic)

class Classification(AnalysisRunner):
    def run_english(self):
        main('english')
    def run_chinese(self):
        main('chinese')

