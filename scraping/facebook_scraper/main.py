from fb import FacebookScraper
import json

if __name__ == "__main__":
    token = ""
    with open('params.json') as fin:
        obj = json.loads(fin.read())
        token = obj["token"]

    fs = FacebookScraper("EAACEdEose0cBAC8Eru7PlDLhWWVhHu00KknyhjejJ4PxoZAmzFqwMNkXTK6iAxO2YeqPI9eeMJDXlJQsn1ZAe8Ngae06aDQ1pXm8lXWZCFqHsHarjScZCewaoGiUDBfLZADSukju0VZAfN22s5Ja429PqhYWradJrYcQ54VrmGETnYnEIH5y9KlPZCzZASIO6ryStGRpLLnCpqPcJ52YlSZBn")

    # facebook date format 2018-03-03T03:01:00+0000 YYYY-MM-DDTHH:mm:ss+0000 <-- UTC time, have to +8 for local time
    start_date = "2018-01-01T00:00:00+0000"
    end_date = "2018-03-03T23:00:00+0000"

    print("From: %s   To: %s", start_date, end_date)
    fs.get_posts(["47298465905"], start_date, end_date, verbose=True)
    fs.get_comments(verbose=True)

    print("%d posts scraped" % len(fs.posts))
    output = {'data': fs.posts}

    output_filename = "fb__%s__to__%s.json" % (start_date, end_date)

    with open(output_filename, "w") as fout:
        fout.write(json.dumps(output))