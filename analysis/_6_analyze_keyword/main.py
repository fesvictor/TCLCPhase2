import json
import operator
from analysis.libs.load_posts import load_posts
from analysis.libs.AnalysisRunner import AnalysisRunner
from analysis.libs.log import log
from analysis._6_analyze_keyword.load_semantic_keywords_processor import load_semantic_keywords_processor


def main(
        language, 
        number_of_keywords_to_be_shown, 
        semantic_type
    ):
    log(f'Analyzing {semantic_type} keywords for {language} data', 1)

    if semantic_type == 'positive':
        keyword_processor = load_semantic_keywords_processor(True, False) 
    elif semantic_type == 'negative':
        keyword_processor = load_semantic_keywords_processor(False, True) 
    else:
        raise Exception("Invalid argument")
    
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

    file_name = f'analysis/_6_analyze_keyword/{language}_top_{semantic_type}_keywords.txt'
    with open(file_name, 'w') as file:
        for value in y_labels:
            file.write(value + "\n")
    log(f'Top 100 keywords are save as {file_name}', 2)

    log('Plotting graph', 2)
    plot_hbar(y_labels, x_values, f'{semantic_type} keyword frequencies')
    log('DONE', 1)



def plot_hbar(y_labels, x_values, title):
    import matplotlib.pyplot as plt
    import numpy as np

    # Fixing random state for reproducibility

    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(19, 20)

    y_pos = np.arange(len(y_labels))
    error = np.random.rand(len(y_labels))
    ax.barh(y_pos, x_values, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Frequencies')
    ax.set_title(title)

    plt.show()


class AnalyzeKeyword(AnalysisRunner):
    def run_english(self):
        main('english', 100, 'positive')
        main('english', 100, 'negative')

    def run_chinese(self):
        main('chinese', 100, 'positive')
        main('chinese', 100, 'negative')


AnalyzeKeyword().run()
