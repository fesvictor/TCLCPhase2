import json
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse
from datetime import timedelta


def plot_graph(language, START_DATE, END_DATE):
    print("Plotting graph . . .")
    with open(f'analysis/_5_analyze_source/{language}_source.json', 'r') as f:
        dic = json.load(f)
        for name in dic:
            y = np.array(dic[name])
            plt.plot(y, label=name)
        xs, ticks = build_xticks(START_DATE, END_DATE)
        plt.xticks(xs, ticks)
        plt.title(
            f"Scraped-result weightage from various sources ({language})")
        plt.xlabel(
            f"Month (e.g. 1 means January) [start={START_DATE},end={END_DATE}]")
        plt.ylabel("Frequency")
        plt.legend()
        plt.savefig("analysis/_5_analyze_source/filtered_chinese_source.png")
        # plt.show()


def build_xticks(start_date, end_date):
    current_date = parse(start_date)
    end = parse(end_date)
    xs = []
    ticks = []
    i = 0
    while current_date < end:
        if current_date.day == 1:
            xs.append(i)
            ticks.append(str(current_date.month))
        current_date += timedelta(days=1)
        i += 1
    return xs, ticks
