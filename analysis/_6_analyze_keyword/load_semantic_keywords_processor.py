def load_semantic_keywords_processor(date='', load_positive = True, load_negative = True, language='english'):
    """
    [Load semantic keywords into FlashText keyword processor and returns it]
    Arguments:
        date {str} -- [YYYYMMDD, must be suffixed with underscore. Example: '20180303_']
    
    Keyword Arguments:
        load_positive {bool} -- [Set true to load positive keywords] (default: {True})
        load_negative {bool} -- [Set true to load negataive keywords] (default: {True})
        language {str} -- [Either 'english' or 'chinese'] (default: {'english'})
    
    Returns:
        [type] -- [description]
        flashtext KeywordProcessor
    """
    from flashtext import KeywordProcessor
    kp = KeywordProcessor()
    positive_words = open(f'keywords/polarity/{date}{language}_positive.txt')
    negative_words = open(f'keywords/polarity/{date}{language}_negative.txt')
    semantic_keywords = []
    if load_positive:
        semantic_keywords += [x.strip() for x in positive_words.read().split('\n')]
    if load_negative:
        semantic_keywords += [x.strip() for x in negative_words.read().split('\n')]
    semantic_keywords = [x.lower() for x in semantic_keywords if len(x) > 0 and not x.startswith(';')]
    for word in semantic_keywords:
        kp.add_keyword(word)
    return kp