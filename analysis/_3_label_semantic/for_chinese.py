from analysis.libs.save_posts import save_posts
from analysis.libs.load_posts import load_posts
from analysis._3_label_semantic.load_semantic_keywords import load_semantic_keywords
from analysis._6_analyze_keyword.load_semantic_keywords_processor import load_semantic_keywords_processor

def for_chinese():
    print(f'Parsing chinese data')
    all_posts = load_posts('analysis/_2_remove_unrelated_data/chinese.json')
    positive_kp = load_semantic_keywords_processor(True, False)
    negative_kp = load_semantic_keywords_processor(False, True)

    for p in all_posts:
        matching_positive_keywords = positive_kp.extract_keywords(p["value"])
        matching_negative_keywords = negative_kp.extract_keywords(p["value"])
        if(len(matching_positive_keywords) > 0):
            p["semantic_value"]["positive"] = True
        if(len(matching_negative_keywords) > 0):
            p["semantic_value"]["negative"] = True

    save_posts(all_posts, f'analysis/_3_label_semantic/chinese.json')    

def obsoleted_for_chinese():
    print(f'Parsing chinese data')
    input_dir = f'analysis/_2_remove_unrelated_data/chinese.json'
    all_posts = load_posts(input_dir)
    keyword_dir = 'keywords/polarity/'
    positive_keywords = load_semantic_keywords(keyword_dir + f'chinese_positive.txt', 'positive')
    negative_keywords = load_semantic_keywords(
        keyword_dir + f'chinese_negative.txt', 'negative')
    all_keywords = positive_keywords + negative_keywords
    for post in all_posts:
        for keyword in all_keywords:
            if keyword['word'] in post['value']:
                post['semantic_value'][keyword['value']] = True
    save_posts(all_posts, f'analysis/_3_label_semantic/chinese.json')
