from analysis._1_process_raw_data.parse_carinet import parse_carinet


def test_parse_carinet_1():
    result = parse_carinet(
        '../sample_data/carinet_20170103_油站在31日晚就悄悄涨价？网友投诉午夜12点前竟打了贵油！.csv')
    assert len(result) == 23
    assert result[0].__dict__ == {
        'date': '20170103',
        'value': '油站在31日晚就悄悄涨价？网友投诉午夜12点前竟打了贵油！',
        'origin': "",
        'source': 'carinet',
        'related_to': None,
        'semantic_value': {'positive': False, 'negative': False}
    }
    assert result[-1].__dict__ == {
        'date': '20170105',
        'value': '时间未到就起价，不可能电脑问题吧',
        'origin': "",
        'source': 'carinet',
        'related_to': None,
        'semantic_value': {'positive': False, 'negative': False}
    }
