def replace_synonyms(posts_str, keywords):
    result = posts_str
    for words in keywords:
        if len(words) > 1:
            for i in range(len(words)):
                if i == 0:
                    continue
                result = result.replace(words[i], words[0])
    return result
                        
