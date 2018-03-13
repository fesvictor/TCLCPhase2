from os import listdir
from collections import OrderedDict
from hanziconv import HanziConv
from analysis.libs.AnalysisRunner import AnalysisRunner
from analysis.libs.log import log
from analysis._2_remove_unrelated_data.load_labels import load_labels
from analysis._2_remove_unrelated_data.label_post import label_post
from analysis._2_remove_unrelated_data.for_english import for_english
from analysis._2_remove_unrelated_data.for_chinese import for_chinese
from analysis.libs.load_posts import load_posts
from analysis.libs.save_posts import save_posts


def main(language):
    log(f"Loading {language} posts", 1)
    posts = load_posts(f'analysis/_1_process_raw_data/output/{language}.json')

    labels = get_labels(language)
    label_post(posts, labels)
    log(f"Removing unrelated posts", 1)
    purified = [x for x in posts if len(x['related_to']) > 0]
    log(f"Number of removed posts = " + str(len(posts) - len(purified)), 1)
    save_posts(purified, f'analysis/_2_remove_unrelated_data/{language}.json')
    SAVE_DUMPED_POST = False
    if SAVE_DUMPED_POST:
        dumped = [x for x in posts if len(x['related_to']) <= 0]
        save_posts(
            dumped, f'analysis/_2_remove_unrelated_data/dumped_{language}.json')


def get_labels(language):
    labels_dir = 'keywords/target/'
    leaders = load_labels(labels_dir + f'leader.json', language)
    parties = load_labels(labels_dir + f'party.json', language)
    if language == 'english':
        return (leaders + parties)
    elif language == 'chinese':
        simplified = list(map(HanziConv.toSimplified, (leaders + parties)))
        return list(OrderedDict.fromkeys(simplified))

class RemoveUnrelatedData(AnalysisRunner):
    def run_english(self):
        for_english()
    def run_chinese(self):
        for_chinese()

RemoveUnrelatedData().run()


