from analysis._6_analyze_keyword.load_semantic_keywords_processor import load_semantic_keywords_processor
from analysis.libs.load_posts import load_posts
from analysis.libs.log import log
from analysis.libs.save_posts import save_posts

def for_chinese(date):
    """[summary]
    
    Arguments:
        date {str} -- Must be prefixed with underscore, e.g. '20180303_' 
    """
    all_posts = load_posts('analysis/_2_remove_unrelated_data/chinese.json')
    positive_kp = load_semantic_keywords_processor(date, True, False)
    negative_kp = load_semantic_keywords_processor(date, False, True)

    log("Labelling semantic of chinese post", 1)
    for p in all_posts:
        matching_positive_keywords = positive_kp.extract_keywords(p["value"])
        matching_negative_keywords = negative_kp.extract_keywords(p["value"])
        if(len(matching_positive_keywords) > 0):
            p["semantic_value"]["positive"] = True
        if(len(matching_negative_keywords) > 0):
            p["semantic_value"]["negative"] = True

    save_posts(all_posts, f'analysis/_3_label_semantic/chinese.json')    