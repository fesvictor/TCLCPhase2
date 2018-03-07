from analysis.load_posts import load_posts
from analysis.using_fasttext.flatten import flatten

posts = load_posts(f'analysis/using_fasttext/labelled_english_posts.json')
flattened = flatten(posts)
print(flattened)