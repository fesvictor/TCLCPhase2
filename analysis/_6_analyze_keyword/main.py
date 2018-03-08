import json
import operator
from analysis.load_posts import load_posts


def main(language):
    semantic_keywords = load_semantic_keywords(language)
    posts = load_posts(f'analysis/_3_label_semantic/{language}.json')
    dic = {}
    for k in semantic_keywords:
        for p in posts:
            if k in p["value"]:
                if k not in dic:
                    dic[k] = []
                dic[k].append(p["origin"])
    json.dump(dic, open(f'analysis/_6_analyze_keyword/{language}_keyword_freq.json', 'w'), ensure_ascii=False)    

    flattened_dic = {}
    for key in dic:
        flattened_dic[key] = len(dic[key])
    
    tuples = sorted(flattened_dic.items(), key=operator.itemgetter(1), reverse=True)
    
    y_labels = []
    x_values = []
    for t in tuples:
        y_labels.append(t[0])
        x_values.append(t[1])

    plot_hbar(y_labels, x_values)
    


def load_semantic_keywords(language):
    file1 = open(f'keywords/polarity/{language}_positive.txt')
    file2 = open(f'keywords/polarity/{language}_negative.txt')
    semantic_keywords = [x.strip() for x in file1.read().split('\n')]
    semantic_keywords += [x.strip() for x in file2.read().split('\n')]
    semantic_keywords = [x.lower() for x in semantic_keywords if len(x) > 0 and not x.startswith(';')]
    return semantic_keywords

def plot_hbar(y_labels, x_values):
    import matplotlib.pyplot as plt
    import numpy as np

    # Fixing random state for reproducibility
    np.random.seed(19680801)


    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 20)


    y_pos = np.arange(len(y_labels))
    error = np.random.rand(len(y_labels))
    ax.barh(y_pos, x_values, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Frequencies')
    ax.set_title('Keyword frequencies')

    plt.show()

main('english')
main('chinese')