from analysis.load_posts import load_posts
from analysis.using_fasttext.flatten import flatten
from analysis.using_fasttext.labelize_using_fasttextformat import labelize_using_fasttextformat

posts = load_posts(f'analysis/using_fasttext/labelled_english_posts.json')
labelled = labelize_using_fasttextformat(posts)
# flattened = flatten(posts)
print(labelled)