import json
from analysis.libs.log import log

def save_posts(list_of_posts, file_name):
    log("Saving output to " + file_name, 1)
    with open(file_name, 'w+', encoding='utf-8') as file:
        if hasattr(list_of_posts[0], '__dict__'):
            json.dump([ob.__dict__ for ob in list_of_posts], file, indent=4, ensure_ascii=False)
        else:
            json.dump([ob for ob in list_of_posts], file, indent=4, ensure_ascii=False)
