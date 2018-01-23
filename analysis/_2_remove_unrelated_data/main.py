from os import listdir
from collections import OrderedDict
from hanziconv import HanziConv
from analysis_process.log import log
from analysis_process._2_remove_unrelated_data.load_labels import load_labels
from analysis_process._2_remove_unrelated_data.label_post import label_post
from analysis_process.load_posts import load_posts
from analysis_process.save_posts import save_posts


def main():
    log("Loading english posts", 1)
    english_posts = load_posts('analysis_process/_1_process_raw_data/output/english.json')
    english_labels = get_english_labels()
    label_post(english_posts, english_labels)
    log("Removing unrelated posts", 1)
    purified = [x for x in english_posts if len(x['related_to']) > 0]
    log("Number of removed posts = " + str(len(english_posts) - len(purified)), 1)
    save_posts(purified, 'analysis_process/_2_remove_unrelated_data/english.json')

    log("Loading chinese posts", 1)
    chinese_posts = load_posts('analysis_process/_1_process_raw_data/output/chinese.json')
    chinese_labels = get_chinese_labels()
    label_post(chinese_posts, chinese_labels)
    log("Removing unrelated posts", 1)
    purified = [x for x in chinese_posts if len(x['related_to']) > 0]
    log("Number of removed posts = " + str(len(chinese_posts) - len(purified)), 1)
    save_posts(purified, 'analysis_process/_2_remove_unrelated_data/chinese.json')
    log("DONE.", 1)


def get_english_labels():
    log("Loading english labels", 1)
    labels_dir = 'data/target/'
    leaders = load_labels(labels_dir + 'leader.txt')
    parties = load_labels(labels_dir + 'party.txt')
    return leaders + parties

def get_chinese_labels():
    log("Loading chinese labels", 1)
    labels_dir = 'data/target/'
    leaders = load_labels(labels_dir + 'chinese_leader.txt')
    parties = load_labels(labels_dir + 'chinese_party.txt')
    simplified = list(map(HanziConv.toSimplified, leaders + parties))
    return list(OrderedDict.fromkeys(simplified))

main()
