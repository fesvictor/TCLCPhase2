from analysis._2_remove_unrelated_data.load_labels import load_labels
from analysis._2_remove_unrelated_data.load_labels import flatten



def test_load_labels_1():
    leaders = load_labels('../sample_label/leader.txt')

    assert leaders == [['纳吉·阿都拉萨', '纳吉'], ['lim guan eng'], ['lim kit siang'],
                       ['mahathir'], ['najib'], ['baby', 'babe']]


def test_load_labels_2():
    parties = load_labels('../sample_label/party.txt')
    assert parties == [['amanah',  'aiyo'], ['bn'],
                       ['dap', 'dalap'], ['gerakan'], ['keadilan']]


def test_flatten_1():
    list = [['amanah',  'aiyo'], ['bn'], [
        'dap', 'dalap'], ['gerakan'], ['keadilan']]
    assert flatten(list) == ['amanah',  'aiyo', 'bn',
                             'dap', 'dalap', 'gerakan', 'keadilan']
