from analysis_process.log import log
import json


def load_posts(file_path):
    log("Loading posts from " + file_path, 1)
    with open(file_path) as file:
        posts = json.load(file)
        return posts