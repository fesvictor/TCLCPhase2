from analysis_process._1_process_raw_data.parse_twitter import parse_twitter


def test1():
    # twitter1.csv contains header of '>>>> HEAD'
    result = parse_twitter('../sample_data/twitter1.csv')
    assert len(result) == 4

def test2():
    # twitter2.csv DOES NOT contains header of '>>>> HEAD'
    result = parse_twitter('../sample_data/twitter2.csv')
    assert len(result) == 4

