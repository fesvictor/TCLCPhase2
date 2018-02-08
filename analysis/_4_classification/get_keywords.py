from analysis.log import log
from hanziconv import HanziConv
import json

def get_keywords(language, keywords_dir='keywords/target/'):
    keywords = []
    log(f"Loading {language} labels", 1)
    for filename in ['leader.json' , 'party.json']:
        dic = json.load(open(keywords_dir + filename))
        if language == 'english':
            for key in dic:
                keywords.append([key] + dic[key]['alias_en'])
        elif language == 'chinese':
            for key in dic:
                keywords.append([dic[key]['name_cn']] + dic[key]['alias_cn'])
            keywords = [x for x in keywords if x != [None]]
    if language == 'english':
        return keywords
    elif language == 'chinese':
        simplified = (HanziConv.toSimplified(str(keywords)))
        return eval(simplified)
