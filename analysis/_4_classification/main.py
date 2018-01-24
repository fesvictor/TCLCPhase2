from analysis._4_classification.standardize_date_format import standardize_date_format
from analysis.load_posts import load_posts
from analysis.log import log
from analysis.save_posts import save_posts


def main(language):
    log(f"Standardizing date format of each {language} posts", 0)
    input_dir = f'analysis/_3_label_semantic/{language}.json'
    all_posts = load_posts(input_dir)
    standardized = standardize_date_format(all_posts)
    log(f"Sorting post based on date", 1)
    sorted_posts = sorted(standardized, key=lambda x: x['date'])
    save_posts(sorted_posts, f'analysis/_4_classification/output/{language}.json')


main('english')
main('chinese')
