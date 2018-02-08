import json 
def check_english():
    leader = json.load(open('../keywords/target/leader.json'))
    leader = [keys for keys in leader]
    party = json.load(open('../keywords/target/party.json'))
    party = [keys for keys in party]
    keywords = leader + party
    english_extracted = open('./results/english_extracted.json').read()
    word_not_found = []
    for word in keywords:
        if word not in english_extracted:
            word_not_found.append(word)

    print("The following keywords are not found in english_extracted.json")
    import pprint
    pprint.pprint(word_not_found)

def check_chinese():
    leader = json.load(open('../keywords/target/leader.json'))
    leader_keys = [keys for keys in leader]
    party = json.load(open('../keywords/target/party.json'))
    party_keys = [keys for keys in party]
    leader = [leader[key]['name_cn'] for key in leader_keys]
    party = [party[key]['name_cn'] for key in party_keys]
    keywords = [x for x in (leader + party) if x is not None]
    chinese_extracted = open('./results/chinese_extracted.json').read()
    word_not_found = []
    for word in keywords:
        if word not in chinese_extracted:
            word_not_found.append(word)

    print("The following keywords are not found in chinese_extracted.json")
    import pprint
    pprint.pprint(word_not_found)

check_english()
check_chinese()
