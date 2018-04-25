from dateutil.parser import parse
from datetime import timedelta


def extract_data(all_posts, start_date, end_date, language):
    # format of start_date OR end_date is string as in 'yyyyddmm', e.g. '20171231'
    # The output should be as stated in ./analysis/README.md
    start = parse(start_date)
    end = parse(end_date)
    length = (end - start).days + 1
    filtered = [x for x in all_posts if start_date <= x['date'] <= end_date]
    data = {} 
    index = 0
    labels = ['positive', 'negative']
    current = start
    for post in filtered:
        if post['date'] != current.strftime("%Y%m%d"):
            current += timedelta(days=1)
            index += 1
            if index >= length:
                break
        for name in post['related_to']:
            if not name in data:
                data[name] = create_semantic_object(length)
            for label in labels:
                if post['semantic_value'][label] is True:
                    data[name][label][index] += 1
            if post['semantic_value']['positive'] is False and post['semantic_value']['negative'] is False:
                data[name]['neutral'][index] += 1

    return {
        'start_date': start_date,
        'end_date': end_date,
        'language': language,
        'data': data
    }

def create_semantic_object(length):
    return {
        'positive': [0] * length,
        'negative': [0] * length,
        'neutral': [0] * length
    }
