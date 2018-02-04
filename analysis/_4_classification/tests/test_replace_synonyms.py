from analysis._4_classification.replace_synonyms import replace_synonyms

mock_input = "{value:'...',related_to:['mo1', 'dap', '阿鸡', '纳吉哥', '纳吉']}"


def test_replace_synonyms():
    output = replace_synonyms(
        mock_input, [['najib', 'mo1'], ['dap'], ['纳吉哥', '纳吉', '阿鸡']])
    assert output == "{value:'...',related_to:['najib', 'dap', '纳吉哥', '纳吉哥', '纳吉哥']}"
