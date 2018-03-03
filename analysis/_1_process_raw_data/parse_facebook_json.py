import json
from analysis.Post import Post

# ASSUMPTIONS:
# - I assume that data without the key "message" will have the key "story"
# - I also assume that data with key "story" contain meaningless message
# - e.g. MalaysiaKini have posted a photo
# Thus, I will ignore data that contain key "story"

def parse_facebook_json(file_path):
    result = []
    if not file_path.endswith('.json'):
        return result
    with open(file_path, 'r') as jsonfile:
        res = json.load(jsonfile)
        result += translate_data_to_post(res['data'])
    return result

def translate_data_to_post(data_list):
    result = []
    if data_list is None:
        return result
    for data in data_list:
        if "message" in data:
            p = Post()
            p.date = data["created_time"]
            p.value = str.lower(data["message"])
            p.source = "facebook-json"
            result.append(p)
        if "comments" in data and len(data["comments"]) > 0:
            result += translate_data_to_post(data["comments"])
    return result