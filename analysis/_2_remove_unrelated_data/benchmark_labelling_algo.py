STR = "who lives in a pineapple under the sea? najib"
LABELS = ["najib", "under", "who"]
def using_regex():
    import re
    for l in LABELS:
        pattern = f"(^|[^a-z]){l}([^a-z]|$)"
        if re.search(pattern, STR) is not None:
            pass


def using_tokens_and_dic():
    tokens = STR.split(" ");
    dic = {}
    for l in LABELS:
        dic[l] = 1
    for tok in tokens:
        if dic.get(tok):
            pass
    


from timeit import timeit
print(timeit(using_regex))
print(timeit(using_tokens_and_dic))
