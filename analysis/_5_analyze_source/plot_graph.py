import json
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse
from datetime import timedelta

START_DATE = '20120601'
END_DATE = '20180131'


def plot_graph(language):
    print("Plotting graph . . .")
    with open(f'{language}_source.json', 'r') as f:
        dic = json.load(f)
        for name in dic:
            y = np.array(dic[name])
            plt.plot(y, label=name)
        xs, ticks = build_xticks(START_DATE, END_DATE)
        plt.xticks(xs, ticks)
        plt.title("Scraped-result weightage from various sources")
        plt.xlabel(
            f"Month (e.g. 1 means January) [start={'20170101'},end={END_DATE}]")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()


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
