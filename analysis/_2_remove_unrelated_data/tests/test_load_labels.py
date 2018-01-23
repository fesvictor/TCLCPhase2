from analysis_process._2_remove_unrelated_data.load_labels import load_labels


def test1():
    leaders = load_labels('../sample_label/leader.txt')
    assert leaders == ['lim guan eng', 'lim kit siang', 'mahathir', 'najib']


def test2():
    parties = load_labels('../sample_label/party.txt')
    assert parties == ['amanah', 'bn', 'dap', 'gerakan', 'keadilan']
