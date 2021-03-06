import json
from analysis.libs.save_posts import save_posts
from analysis.libs.load_posts import load_posts
from flashtext import KeywordProcessor

from analysis.libs.log import log
from analysis.libs.load_posts import load_posts
from flashtext import KeywordProcessor


def for_english():
    # all_posts = load_posts('analysis/_2_remove_unrelated_data/english.json') # this line is to check whether this new algorithm differ from the previous algo
    all_posts = load_posts('analysis/_1_process_raw_data/output/english.json')
    leaders = json.load(open(f'keywords/target/leader.json'))
    parties = json.load(open(f'keywords/target/party.json'))
    combined = {**leaders, **parties}
    keyword_dict = {}
    for key, value in combined.items():
        keyword_dict[key] = [key] + combined[key]["alias_en"]

    kp = KeywordProcessor()
    kp.add_keywords_from_dict(keyword_dict)
    for p in all_posts:
        p["related_to"] = list(set(kp.extract_keywords(p["value"])))

    purified = [x for x in all_posts if len(x['related_to']) > 0]
    log(f"Number of removed posts = " + str(len(all_posts) - len(purified)), 1)

    save_posts(purified, f'analysis/_2_remove_unrelated_data/english.json')
