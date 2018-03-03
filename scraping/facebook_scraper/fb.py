import facebook
from dateutil import parser

def date_in_range(target_date, start_date, end_date):
    #print(target_date, start_date, end_date)
    td = parser.parse(target_date)
    sd = parser.parse(start_date)
    ed = parser.parse(end_date)

    tdi = int(td.timestamp())
    sdi = int(sd.timestamp())
    edi = int(ed.timestamp())

    #print(sdi, tdi, edi, sdi <= tdi <= edi)

    return sdi <= tdi <= edi
    
def strip_next_page_token(url):
    return url.split("after=")[1]

class FacebookScraper:
    def __init__(self, token):
        self.graph = facebook.GraphAPI(access_token=token, version="2.11")

    def get_posts(self, page_ids, start_date, end_date, verbose=False):
        self.posts_list = []        
        for page_id in page_ids:
            cursor = self.graph.get_object(id=page_id, fields="posts.limit(100)")
            
            posts = []

            filter_stop = False

            counter = 0
            print("Getting posts")


            while "next" in cursor["posts"]["paging"]:
                next_page = strip_next_page_token(cursor["posts"]["paging"]["next"])

                # Prepare data for time check
                last_post_time = cursor["posts"]["data"][0]["created_time"]

                for post in cursor["posts"]["data"]:
                    if date_in_range(post["created_time"], start_date, end_date):
                        post["created_time"] = int(parser.parse(post["created_time"]).timestamp())
                        posts.append(post)

                if verbose:
                    counter = len(posts)
                    print("Current # of posts: %d" % (counter))

                if date_in_range(last_post_time, start_date, end_date):
                    cursor = self.graph.get_object(id=page_id, fields="posts.limit(100).after(%s)" % (next_page))
                else:
                    filter_stop = True
                    break
            
            # Take the last post because it is the end of all posts from the page
            # and not stop because of filter
            if not filter_stop:
                posts += cursor["posts"]["data"]

            self.posts_list = posts

    def get_comments(self, verbose=False):
        if not hasattr(self, 'posts_list'):
            raise Exception("get_posts is not ran yet")

        posts = []
        counter = 1
        for post in self.posts_list:
            post_id = post["id"]

            if verbose:
                print("%5d/%5d" % (counter, len(self.posts_list)), post_id)
                counter += 1

            cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100)")
            comments = []

            if "comments" in cursor:
                while "next" in cursor["comments"]["paging"]:
                    next_page = strip_next_page_token(cursor["comments"]["paging"]["next"])
                    _comments = cursor["comments"]["data"]

                    for _comment in _comments:
                        _comment["created_time"] = int(parser.parse(_comment["created_time"]).timestamp())
                    comments += _comments

                    cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100).after(%s)" % (next_page))

            post["comments"] = comments
            posts.append(post)
        
        self.posts = posts