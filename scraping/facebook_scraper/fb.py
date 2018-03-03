import facebook
from dateutil import parser

def date_in_range(target_date, start_date, end_date):
    td = parser.parse(target_date)
    sd = parser.parse(start_date)
    ed = parser.parse(end_date)

    tdi = int(td.timestamp())
    sdi = int(sd.timestamp())
    edi = int(ed.timestamp())

    return sdi < tdi < edi
    

class FacebookScraper:
    def __init__(self, token):
        self.graph = facebook.GraphAPI(access_token=token, version="2.11")

    def get_posts(self, page_id, start_date, end_date):
        cursor = self.graph.get_object(id=page_id, fields="posts.limit(100)")
        
        posts = []

        filter_stop = False
        while "next" in cursor["posts"]["paging"]:
            next_page = cursor["posts"]["paging"]["next"]

            # Prepare data for time check
            last_post_time = cursor["posts"]["data"][-1]["created_date"]

            if date_in_range(last_post_time, start_date, end_date):
                posts.append(cursor["posts"]["data"])
                cursor = self.graph.get_object(id=page_id, fields="posts.limit(100).after(%s)" % (next_page))
            else:
                filter_stop = True
                break
        
        # Take the last post because it is the end of all posts from the page
        # and not stop because of filter
        if not filter_stop:
            posts.append(cursor["posts"]["data"])

        self.posts_list = posts

    def get_comments(self):
        if not hasattr(self, 'posts_list'):
            return None

        posts = []
        for post in self.posts_list:
            post_id = post["id"]
            cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100)")

            while "next" in cursor["comments"]["paging"]:
                


