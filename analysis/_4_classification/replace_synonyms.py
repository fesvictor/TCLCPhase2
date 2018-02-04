def replace_synonyms(posts_str, keywords):
    result = posts_str
    for words in keywords:
        if len(words) > 1:
            stdout = f"Replacing ["
            for i in range(len(words)):
                if i == 0:
                    continue
                stdout += f" {words[i]}, "
                result = result.replace(f"'{words[i]}'", f"'{words[0]}'")
            stdout += "] with " + words[0]
            print(stdout)
    return result
                        
