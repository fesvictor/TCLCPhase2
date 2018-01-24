from analysis.save_posts import save_posts
from analysis.load_posts import load_posts


def main():
    print("Parsing english data")
    input_dir = 'analysis/_2_remove_unrelated_data/english.json'
    all_posts = load_posts(input_dir)
    keyword_dir = 'data/categories/polarity/'
    positive_keywords = load_keywords(keyword_dir + 'positive.txt', 'positive')
    negative_keywords = load_keywords(keyword_dir + 'negative.txt', 'negative')
    all_keywords = positive_keywords + negative_keywords
    for post in all_posts:
        for keyword in all_keywords:
            if keyword['word'] in post['value']:
                post['semantic_value'][keyword['value']] = True
    save_posts(all_posts, 'analysis/_3_label_semantic/english.json')

    #TODO: Label semantic of chinese data


def load_keywords(file_path, semantic_value):
    result = []
    with open(file_path) as file:
        for word in file:
            result.append({
                'word': word.rstrip('\n').strip(),
                'value': semantic_value # positive OR negative OR neutral
            })
    return result


main()
