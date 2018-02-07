from analysis._1_process_raw_data.parse_blog import parse_blog


def test1():
    result = parse_blog('../sample_data/blog.csv')
    print(result[0].__dict__)
    assert result[0].__dict__ == {
        'date': "20170723",
        'value': "mahathir's cronies vs najib's cronies",
        'origin': "",
        'source': "blog",
        'related_to': None,
        'semantic_value': {
            'positive': False,
            'negative': False
        }
    }
