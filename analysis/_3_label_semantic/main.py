from analysis.save_posts import save_posts
from analysis.load_posts import load_posts


def main(language):
    print(f'Parsing {language} data')
    input_dir = f'analysis/_2_remove_unrelated_data/{language}.json'
    all_posts = load_posts(input_dir)
    keyword_dir = 'keywords/polarity/'
    positive_keywords = load_keywords(keyword_dir + f'{language}_positive.txt', 'positive')
    negative_keywords = load_keywords(keyword_dir + f'{language}_negative.txt', 'negative')
    all_keywords = positive_keywords + negative_keywords
    for post in all_posts:
        for keyword in all_keywords:
            if keyword['word'] in post['value']:
                post['semantic_value'][keyword['value']] = True
    save_posts(all_posts, f'analysis/_3_label_semantic/{language}.json')


def load_keywords(file_path, semantic_value):
    result = []
    with open(file_path, encoding='utf8') as file:
        for word in file:
            result.append({
                'word': word.rstrip('\n').strip().lower(),
                'value': semantic_value # positive OR negative OR neutral
            })
    return result


main('english')
main('chinese')
