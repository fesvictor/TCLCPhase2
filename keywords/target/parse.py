from hanziconv import HanziConv
def create_object():
    return {
        'name_cn': None,
        'parent_party': None,
        'alias_en': [],
        'alias_cn': []
    }

# def isEnglish(s):
#     try:
#         s.encode(encoding='utf-8').decode('ascii')
#     except UnicodeDecodeError:
#         return False
#     else:
#         return True

def map_name(type):
    import json
    with open(f'./{type}.json', 'r') as lfile:
        leaders = json.load(lfile)
        with open('../../visualization/name_mapping.csv') as nfile:
            for line in nfile:
                toks = [x.strip() for x in line.split(',')]
                english_name = toks[0]
                chinese_name = HanziConv.toSimplified(toks[1])
                if(leaders.get(english_name)):
                    if(len(chinese_name) > 0):
                        leaders[english_name]['name_cn'] = chinese_name
                    if(leaders.get(chinese_name)):
                        leaders[english_name]['alias_cn'] = leaders[chinese_name]['alias_cn']
                        leaders.pop(chinese_name)

    with open(f'./{type}.json', 'w') as file:
        import json
        json.dump(leaders, file, indent=4, ensure_ascii=False)

# map_name('party') 
# map_name('leader')


# with open('./party.json', 'w') as file:
#     json.dump([ob for ob in res], file, indent=4, ensure_ascii=False)


#                 # if(isEnglish(tok)):
#                 #     matched = [y for y in leaders if y['name_en'] == tok]
#                 #     if(len(matched) == 0):
#                 #         obj = create_object()
#                 #         obj['name_en'] = tok
#                 # else:
#                 #     tok = HanziConv.toSimplified(tok)
#                 #     matched = [y for y in leaders if y['name_cn'] == tok]
#                 #     if(len(matched) == 0):
#                 #         obj = create_object()
#                 #         obj['name_cn'] = tok
#                 #         leaders.append(obj)

def parse():
    res = {}
    with open('./english_leader.txt', 'r') as file:
        for line in file:
            toks = [x.strip() for x in line.split(',')]
            x = create_object()
            x['alias_en'] += toks[1:]
            res[toks[0]] = x
            
    with open('./chinese_leader.txt', 'r') as file:
        import hanziconv
        for line in file:
            line = hanziconv.HanziConv.toSimplified(line)
            toks = [x.strip() for x in line.split(',')]
            x = create_object()
            x['alias_cn'] += toks[1:]
            res[toks[0]] = x

    with open('./leader.json', 'w') as file:
        import json
        json.dump(res, file, indent=4, ensure_ascii=False)
        
