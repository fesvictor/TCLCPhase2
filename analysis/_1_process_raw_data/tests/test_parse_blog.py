from analysis_process._1_process_raw_data.parse_blog import parse_blog


def test1():
    result = parse_blog('../sample_data/blog.csv')
    assert result[0].__dict__ == {
        'date': "20170723",
        'value': "mahathir's cronies vs najib's cronies",
        'source': "blog",
        'related_to': None,
        'semantic_value': None
    }
