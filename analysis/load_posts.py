from analysis.log import log
import json


def load_posts(file_path):
    log("Loading posts from " + file_path, 1)
    with open(file_path, encoding='utf8') as file:
        posts = json.load(file)
        return posts