def load_semantic_keywords_processor(load_positive = True, load_negative = True):
    from flashtext import KeywordProcessor
    kp = KeywordProcessor()
    file1 = open(f'keywords/polarity/english_positive.txt')
    file2 = open(f'keywords/polarity/english_negative.txt')
    semantic_keywords = []
    if load_positive:
        semantic_keywords += [x.strip() for x in file1.read().split('\n')]
    if load_negative:
        semantic_keywords += [x.strip() for x in file2.read().split('\n')]
    semantic_keywords = [x.lower() for x in semantic_keywords if len(x) > 0 and not x.startswith(';')]
    for word in semantic_keywords:
        kp.add_keyword(word)
    return kp
