from analysis.save_posts import save_posts
from analysis.load_posts import load_posts
from analysis._3_label_semantic.load_semantic_keywords import load_semantic_keywords


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
