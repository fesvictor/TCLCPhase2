def load_semantic_keywords_processor(load_positive = True, load_negative = True, language='english'):
    from flashtext import KeywordProcessor
    kp = KeywordProcessor()
    pos_1 = open(f'keywords/polarity/{language}_positive.txt')
    pos_2 = open(f'keywords/polarity/extra_{language}_positive.txt')
    neg_1 = open(f'keywords/polarity/{language}_negative.txt')
    neg_2 = open(f'keywords/polarity/extra_{language}_negative.txt')
    semantic_keywords = []
    if load_positive:
        semantic_keywords += [x.strip() for x in pos_1.read().split('\n')]
        semantic_keywords += [x.strip() for x in pos_2.read().split('\n')]
    if load_negative:
        semantic_keywords += [x.strip() for x in neg_1.read().split('\n')]
        semantic_keywords += [x.strip() for x in neg_2.read().split('\n')]
    semantic_keywords = [x.lower() for x in semantic_keywords if len(x) > 0 and not x.startswith(';')]
    for word in semantic_keywords:
        kp.add_keyword(word)
    return kp
