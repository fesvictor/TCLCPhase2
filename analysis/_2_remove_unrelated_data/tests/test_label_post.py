from analysis_process._2_remove_unrelated_data.label_post import label_post

sample_posts = [
    {
        "date": "2017-05-18 11:56:09",
        "value": "guan eng friend with najib",
        "source": "facebook",
        "related_to": None,
        "semantic_value": None
    },
    {
        "date": "2017-05-18 08:54:07",
        "value": "let us talks baby",
        "source": "facebook",
        "related_to": None,
        "semantic_value": None
    },
    {
        "date": "2017-05-18 08:54:07",
        "value": "lks lks lks",
        "source": "facebook",
        "related_to": None,
        "semantic_value": None
    }
]

sample_labels = [
    "najib",
    "guan eng",
    "lks"
]


def test_1():
    label_post(sample_posts, sample_labels)
    assert sample_posts[0]['related_to'] == ['najib', 'guan eng']
    assert sample_posts[1]['related_to'] == []
    assert sample_posts[2]['related_to'] == ['lks']
