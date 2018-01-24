from analysis._4_classification.standardize_date_format import correct_date_format_of_facebook
from analysis._4_classification.standardize_date_format import correct_date_format_of_twitter


def test_correct_date_format_of_facebook():
    input = '2017-05-18 06:24:38'
    result = correct_date_format_of_facebook(input)
    assert result == '20170518'


def test_correct_date_format_of_twitter():
    input = 'Wed Jan 1 06:48:37 +0000 2017'
    result = correct_date_format_of_twitter(input)
    assert result == '20170101'
