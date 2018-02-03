from os import listdir
from collections import OrderedDict
from hanziconv import HanziConv
from analysis.log import log
from analysis._2_remove_unrelated_data.load_labels import load_labels
from analysis._2_remove_unrelated_data.label_post import label_post
from analysis.load_posts import load_posts
from analysis.save_posts import save_posts


def main(language):
    log(f"Loading {language} posts", 1)
    posts = load_posts(f'analysis/_1_process_raw_data/output/{language}.json')
    labels = get_labels(language)
    label_post(posts, labels)
    log(f"Removing unrelated posts", 1)
    purified = [x for x in posts if len(x['related_to']) > 0]
    dumped = [x for x in posts if len(x['related_to']) <= 0]
    log(f"Number of removed posts = " + str(len(posts) - len(purified)), 1)
    save_posts(purified, f'analysis/_2_remove_unrelated_data/{language}.json')
    save_posts(dumped, f'analysis/_2_remove_unrelated_data/dumped_{language}.json')


def get_labels(language):
    log(f"Loading {language} labels", 1)
    labels_dir = 'keywords/target/'
    leaders = load_labels(labels_dir + f'{language}_leader.txt')
    parties = load_labels(labels_dir + f'{language}_party.txt')
    if language == 'english':
        return leaders + parties
    elif language == 'chinese':
        simplified = list(map(HanziConv.toSimplified, leaders + parties))
        return list(OrderedDict.fromkeys(simplified))


main('english')
main('chinese')
