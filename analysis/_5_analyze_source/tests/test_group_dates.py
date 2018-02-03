from analysis._5_analyze_source.group_dates import group_dates

def test_group_dates_1():
    start = '20170131'
    end = '20170205'
    dates = ['20170131', '20170201', '20170201', '20170204']
    result = group_dates(start, end, dates)
    assert result == [1, 2, 0, 0, 1, 0]

def test_group_dates_2():
    start = '20170131'
    end = '20170205'
    dates = ['20170201', '20170201', '20170205']
    result = group_dates(start, end, dates)
    assert result == [0, 2, 0, 0, 0, 1]
