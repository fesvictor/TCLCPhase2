from analysis.save_posts import save_posts
from analysis.load_posts import load_posts
from analysis._3_label_semantic.load_semantic_keywords import load_semantic_keywords
from analysis._6_analyze_keyword.load_semantic_keywords_processor import load_semantic_keywords_processor


print(f'Parsing english data')
all_posts = load_posts('analysis/_2_remove_unrelated_data/english.json')
positive_kp = load_semantic_keywords_processor(True, False)
negative_kp = load_semantic_keywords_processor(False, True)

for p in all_posts:
    matching_positive_keywords = positive_kp.extract_keywords(p["value"])
    matching_negative_keywords = negative_kp.extract_keywords(p["value"])
    if(len(matching_positive_keywords) > 0):
        p["semantic_value"]["positive"] = True
    if(len(matching_negative_keywords) > 0):
        p["semantic_value"]["negative"] = True

save_posts(all_posts, f'analysis/_3_label_semantic/english.json')    

