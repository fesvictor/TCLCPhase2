def load_labels(file_path):
    result = []
    with open(file_path, encoding='utf8') as keywords:
        for word in keywords:
            result += [x.strip() for x in word.rstrip('\n').split(',')]
    return result
