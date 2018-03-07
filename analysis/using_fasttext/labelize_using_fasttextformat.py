def labelize_using_fasttextformat(posts):
    results = ""
    for p in posts:
        positive = p["semantic_value"]["positive"]
        negative = p["semantic_value"]["negative"]
        if not positive and not negative:
            results += "__label__neutral "
        if positive:
            results += "__label__positive "
        if negative:
            results += "__label__negative "
        results += p["value"].replace("\n", "") + "\n"
    return results

        