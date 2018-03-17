from fb import FacebookScraper
import json
import pathlib
import os
import notify2

if __name__ == "__main__":
    notify2.init("Facebook scrapper")
    token = ""
    with open('params.json') as fin:
        obj = json.loads(fin.read())
        token = obj["token"]    
        start_date = obj["start_date"]
        end_date = obj["end_date"]
        pages = obj["pages"]


    # facebook date format 2018-03-03T03:01:00+0000 YYYY-MM-DDTHH:mm:ss+0000 <-- UTC time, have to +8 for local time


    print("From: %s   To: %s" % (start_date, end_date))

    for page in pages:
        fs = FacebookScraper(token)
        fs.get_posts([page], start_date, end_date, verbose=True)
        fs.get_comments(verbose=True)

        print("%d posts scraped" % len(fs.posts))
        output = {'data': fs.posts}

        output_filename = "fb__%s__%s__to__%s.json" % (fs.name, start_date, end_date)

        pathlib.Path('data').mkdir(parents=True, exist_ok=True)
        with open(os.path.join('data', output_filename), "w") as fout:
            fout.write(json.dumps(output))