from analysis.load_posts import load_posts
from analysis._4_classification.extract_data import extract_data


def test_extract_data():
    all_output = load_posts('./sample_data/sample.json')
    start_date = '20130303'  # Jan 01
    end_date = '20130309'  # Jan 08
    result = extract_data(all_output, start_date, end_date, 'english')
    assert result == {
        'data': {
            'anwar': {
                'negative': [0, 0, 1, 0, 0, 0, 0],
                'neutral': [0, 0, 0, 0, 0, 0, 0],
                'positive': [1, 1, 1, 0, 1, 1, 2]},
            'najib': {
                'negative': [0, 0, 1, 0, 0, 0, 0],
                'neutral': [0, 1, 0, 0, 0, 0, 0],
                'positive': [1, 0, 1, 0, 1, 1, 2]},
            'pas': {
                'negative': [0, 0, 0, 0, 0, 0, 0],
                'neutral': [0, 0, 0, 1, 0, 0, 0],
                'positive': [0, 0, 0, 0, 0, 0, 0]
            }
        },
        'end_date': '20130309',
        'language': 'english',
        'start_date': '20130303'
    }
