from analysis._4_classification.replace_synonyms import replace_synonyms

mock_input = "{value:'...',related_to:['mo1', 'dap']}"


def test_replace_synonyms():
    output = replace_synonyms(mock_input, [['najib', 'mo1'], ['dap']])
    assert output == "{value:'...',related_to:['najib', 'dap']}"
