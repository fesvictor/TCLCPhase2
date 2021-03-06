import json
import ntpath
from analysis.libs.Post import Post

"""
ASSUMPTIONS:
- I assume that data without the key "message" will have the key "story"
- I also assume that data with key "story" contain meaningless message
- e.g. MalaysiaKini have posted a photo
Thus, I will ignore data that contain key "story".

According to Dr. Victor, he said since post message will be neutral,
we will not get its value, so we will only extract comments at the moment
"""
EXTRACT_POST_MESSAGE = True

def parse_facebook_json(file_path):
    result = []
    if not file_path.endswith('.json'):
        return result
    with open(file_path, 'r') as jsonfile:
        res = json.load(jsonfile)
        result += translate_data_to_post(res['data'], file_path)
    return result

def translate_data_to_post(data_list, file_path):
    result = []
    if data_list is None:
        return result
    for data in data_list:
        if "message" in data and EXTRACT_POST_MESSAGE:
            p = Post()
            p.date = data["created_time"]
            p.value = str.lower(data["message"])
            p.source = '_'.join(ntpath.basename(file_path).split("__")[:2])
            p.origin = file_path
            result.append(p)
        if "comments" in data and len(data["comments"]) > 0:
            result += translate_data_to_post(data["comments"], file_path)
    return result