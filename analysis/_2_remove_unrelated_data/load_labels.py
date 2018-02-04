def load_labels(file_path):
    result = []
    with open(file_path, encoding='utf8') as keywords:
        for word in keywords:
            result.append([x.strip() for x in word.rstrip('\n').replace('\ufeff', '').split(',')])
    return result

def flatten(list):
    return [item for sublist in list for item in sublist]