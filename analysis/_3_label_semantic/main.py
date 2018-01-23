from analysis_process.save_posts import save_posts
from analysis_process.load_posts import load_posts


def main():
    input_dir = 'analysis_process/_2_remove_unrelated_data/output.json'
    all_posts = load_posts(input_dir)
    keyword_dir = 'data/categories/polarity/'
    positive_keywords = load_keywords(keyword_dir + 'positive.txt', 1)
    negative_keywords = load_keywords(keyword_dir + 'negative.txt', -1)
    all_keywords = positive_keywords + negative_keywords
    for post in all_posts:
        post['semantic_value'] = 0
        for keyword in all_keywords:
            if keyword['word'] in post['value']:
                post['semantic_value'] += keyword['value']
    save_posts(all_posts, 'analysis_process/_3_label_semantic/output.json')


def load_keywords(file_path, semantic_value):
    result = []
    with open(file_path) as file:
        for word in file:
            result.append({
                'word': word.rstrip('\n').strip(),
                'value': semantic_value
            })
    return result


main()
