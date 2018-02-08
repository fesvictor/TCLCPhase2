from analysis._4_classification.get_keywords import get_keywords


def test_get_keywords_chinese():
    chinese = get_keywords('chinese', './sample_data/')
    assert chinese == [
        ['纳吉·阿都拉萨', '纳吉', '鸡哥', '1马哥'], 
        ['马哈迪·莫哈末', '马哈迪', '老马', '敦马', '老番薯'],
        ['林吉祥'], 
        ['诚信党'], 
        ['国阵'], 
        ['行动党', '行动党', '行洞党', '火箭', '火贱']
    ]

def test_get_keywords_english():
    english = get_keywords('english', './sample_data/')
    assert english == [
        ['najib', 'mo1', 'pm'], 
        ['mahathir'], 
        ['mahfuz omar'], 
        ['lim kit siang', 'lks'], 
        ['amanah'], 
        ['bn', 'barisan', 'barisan nasional'], 
        ['dap']
    ]