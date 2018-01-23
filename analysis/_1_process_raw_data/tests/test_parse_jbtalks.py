from analysis_process._1_process_raw_data.parse_jbtalks import parse_jbtalks


def test1():
    result = parse_jbtalks(
        "../sample_data/jbtalks_20160329_敦馬 在任時也收過 2億3000萬存巫統基金 .csv")
    assert len(result) == 3
    assert result[0].value.startswith('敦馬')
    assert result[1].source == 'jbtalks'
    assert result[1].date == '20160329'
    assert result[1].value.endswith("《中國報》")
