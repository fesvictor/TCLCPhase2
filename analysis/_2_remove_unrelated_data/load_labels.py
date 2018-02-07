import json


def load_labels(file_path, language):
    result = []
    with open(file_path, encoding='utf8') as file:
        dic = json.load(file)
        for key in dic:
            if language == 'english':
                result.append(key)
                result += dic[key]['alias_en']
            elif language == 'chinese':
                x = dic[key]['name_cn']
                if x is not None:
                    result.append(x)
                result += dic[key]['alias_cn']
            else:
                raise Exception("Invalid language argument. Expected (chinese/english) but got " + language)
    return result

