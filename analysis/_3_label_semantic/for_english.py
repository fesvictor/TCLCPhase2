from analysis._6_analyze_keyword.load_semantic_keywords_processor import load_semantic_keywords_processor
from analysis.libs.load_posts import load_posts
from analysis.libs.log import log
from analysis.libs.save_posts import save_posts

def for_english(date):
    """[summary]
    
    Arguments:
        date {str} -- Must be prefixed with underscore, e.g. '20180303_' 
    """
    all_posts = load_posts('analysis/_2_remove_unrelated_data/english.json')
    log("Searching post that have negated positive words", 2)
    negated_positive_kp = get_negated_postivie_kp(date)
    for p in all_posts:
        if len(negated_positive_kp.extract_keywords(p["value"])) > 0:
            p["semantic_value"]["negative"] = True
    negative_posts = [x for x in all_posts if x["semantic_value"]["negative"] == True]
    remaining_posts = [x for x in all_posts if x["semantic_value"]["negative"] == False]
    log(f"Labelled {len(negative_posts)} as negative posts which are identified by negated positive keywords", 2)
    log(f"{len(remaining_posts)} posts left to be labelled", 2)

    positive_kp = load_semantic_keywords_processor(date, True, False)
    negative_kp = load_semantic_keywords_processor(date, False, True)

    log("Labelling semantic of english post", 1)
    for p in remaining_posts:
        matching_positive_keywords = positive_kp.extract_keywords(p["value"])
        matching_negative_keywords = negative_kp.extract_keywords(p["value"])
        if(len(matching_positive_keywords) > 0):
            p["semantic_value"]["positive"] = True
        if(len(matching_negative_keywords) > 0):
            p["semantic_value"]["negative"] = True

    save_posts(negative_posts + remaining_posts, f'analysis/_3_label_semantic/english.json')    


def get_negated_postivie_kp(date):
    negative_quantifiers = open('keywords/polarity/english_negative_quantifier.txt').read().split('\n')
    negated_positive_kp = load_semantic_keywords_processor(date, True, False)
    for key in negated_positive_kp.get_all_keywords().keys():
        negated_positive_kp.remove_keyword(key)
        for q in negative_quantifiers:
            negated_positive_kp.add_keyword(q + " " + key)
    return negated_positive_kp
