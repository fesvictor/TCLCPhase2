from analysis.libs.load_posts import load_posts
from analysis.libs.save_posts import save_posts


posts = load_posts(f'analysis/using_fasttext/labelled_english_posts.json')
positive = "__label__2"
with open('analysis/using_fasttext/predicted_label.txt') as file:
    labels = file.read().split('\n')
    for i in range(0, len(posts)):
        posts[i]["semantic_value"][("positive" if labels[i] == positive else "negative")] = True

save_posts(posts,'analysis/results/fasttext/english_analyzed.json' )