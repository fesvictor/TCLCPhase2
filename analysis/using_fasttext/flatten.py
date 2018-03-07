def flatten(posts):
    results = ""
    for p in posts:
        results += p['value'].replace("\n", "") + '\n'
    return results