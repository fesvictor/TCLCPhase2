def map_name_from_file(filename):
    name_dict = {}
    with open(filename) as inFile:
        for row in inFile:
            names = row.split(",")
            for name in names:
                name = name.strip('\n')
                name_dict[name] = names[0]
    name_dict.pop('', None)
    return name_dict

import json
def map_name_from_json(filename, language="en", name_dict={}):
    with open(filename) as inFile:
        js = json.load(inFile)

        for k in js:
            if language == "en":
                name_dict[k] = k
                
                for name in js[k]["alias_en"]:
                    name_dict[name] = k
            elif language == "cn":
                # Must map an English to Chinese for params to map to chinese
                name_dict[k] = js[k]["name_cn"]
                name_dict[js[k]["name_cn"]] = js[k]["name_cn"]
                for name in js[k]["alias_cn"]:
                    name_dict[name] = js[k]["name_cn"]


    return name_dict
