from analysis._2_remove_unrelated_data.load_labels import load_labels


def test_load_english_labels():
    labels = load_labels('../sample_label/leader.json', 'english')
    assert labels == ['najib', 'mo1', 'pm', 'mahathir',
                      'mahfuz omar', 'lim kit siang', 'lks']


def test_load_chinese_labels():
    labels = load_labels('../sample_label/leader.json', 'chinese')
    print(labels)
    assert labels == ['纳吉·阿都拉萨', '纳吉', '鸡哥', '1马哥',
                      '马哈迪·莫哈末', '马哈迪', '老马', '敦马', '老番薯', '林吉祥']
