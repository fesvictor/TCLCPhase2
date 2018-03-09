def load_semantic_keywords(file_path, semantic_value):
    result = []
    with open(file_path, encoding='utf8') as file:
        for line in file:
            if line.startswith(';'): # ignore comments
                continue
            result.append({
                'word': line.rstrip('\n').strip().lower(),
                'value': semantic_value # positive OR negative OR neutral
            })
    return result