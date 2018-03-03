from analysis._1_process_raw_data.parse_facebook_csv import parse_facebook_csv
def test1():
    parent_dir = '..'
    file_path = parent_dir + '/sample_data/facebook.csv'
    posts = parse_facebook_csv(file_path)
    assert posts[0].value == "b'report: red granite in talks with doj to settle 1mdb-linked lawsuit'"


