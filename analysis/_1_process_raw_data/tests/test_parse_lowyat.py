from analysis_process._1_process_raw_data.parse_lowyat import parse_lowyat


def test1():
    result = parse_lowyat('../sample_data/lowyat_20170716_4361817_Umno s GE14 Manual is ready  Hishammuddin.csv')
    assert len(result) == 5
    assert result[0].value == 'Umno s GE14 Manual is ready  Hishammuddin'
    assert result[0].date == '20170716'
    assert result[0].source == 'lowyat'
    assert result[1].value.startswith(
        'Umno vice-president Datuk Seri Hishammuddin Hussein meets')
    assert result[1].date == '20170716'
    assert result[1].source == 'lowyat'
