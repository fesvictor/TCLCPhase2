import json
import operator
from analysis.libs.load_posts import load_posts
from analysis._6_analyze_keyword.load_semantic_keywords_processor import load_semantic_keywords_processor


def main(language, number_of_keywords_to_be_shown):
    keyword_processor = load_semantic_keywords_processor()
    posts = load_posts(f'analysis/_3_label_semantic/{language}.json')
    dic = {}
    for p in posts:
        matching_keywords = keyword_processor.extract_keywords(p["value"])
        for word in matching_keywords:
            if not word in dic: 
                dic[word] = []
            dic[word].append(p["origin"])
    
    json.dump(dic, open(
        f'analysis/_6_analyze_keyword/{language}_keyword_freq.json', 'w'), ensure_ascii=False)

    flattened_dic = {}
    for key in dic:
        flattened_dic[key] = len(dic[key])

    tuples = sorted(flattened_dic.items(),
                    key=operator.itemgetter(1), reverse=True)

    y_labels = []
    x_values = []
    for t in tuples:
        y_labels.append(t[0])
        x_values.append(t[1])

    y_labels = y_labels[0: number_of_keywords_to_be_shown + 1]
    x_values = x_values[0: number_of_keywords_to_be_shown + 1]
    plot_hbar(y_labels, x_values)



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


main('english', 30)
# main('chinese')
