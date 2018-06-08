import facebook
import notify2

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

def bypass_date(target_date, end_date):
    td = parser.parse(target_date)
    ed = parser.parse(end_date)

    tdi = int(td.timestamp())
    edi = int(ed.timestamp())
    return edi <= tdi
    
def strip_next_page_token(url):
    return url.split("after=")[1]

class FacebookScraper:
    def __init__(self, token):
        self.access_token = token
        self.graph = facebook.GraphAPI(access_token=token, version="2.12")
        
    def get_posts(self, page_ids, start_date, end_date, verbose=False):
        self.posts_list = []        

        # Try to get the name 
        try:
            self.name = self.graph.get_object(id=page_ids[0], fields="name")["name"]
        except facebook.GraphAPIError:
            self.reinsert_access_token()
            self.name = self.graph.get_object(id=page_ids[0], fields="name")["name"]            

        if verbose:
            print("Scraping from %s" % (self.name))

        for page_id in page_ids:
            try:
                # Get the cursor for the current object
                cursor = self.graph.get_object(id=page_id, fields="posts.limit(100)")
                
                posts = []

                filter_stop = False

                counter = 0
                print("Getting posts")

                bypass = True
                while "next" in cursor["posts"]["paging"]:
                    # Get cursor for next page
                    next_page = strip_next_page_token(cursor["posts"]["paging"]["next"])

                    if bypass:
                        # Ignore date
                        if bypass_date(cursor["posts"]["data"][0]["created_time"], end_date):
                            if verbose:
                                print("Bypassing %s" % (cursor["posts"]["data"][0]["created_time"]))
                            cursor = self.graph.get_object(id=page_id, fields="posts.limit(100).after(%s)" % (next_page))
                            continue
                        else:
                            bypass = False

                    # Prepare data for time check
                    last_post_time = cursor["posts"]["data"][0]["created_time"]

                    for post in cursor["posts"]["data"]:
                        if date_in_range(post["created_time"], start_date, end_date):
                            # Replace time with UNIX time
                            post["created_time"] = int(parser.parse(post["created_time"]).timestamp())
                            posts.append(post)

                    if verbose:
                        counter = len(posts)
                        print("Current # of posts: %d" % (counter))

                    if date_in_range(last_post_time, start_date, end_date):
                        # Enter next object
                        cursor = self.graph.get_object(id=page_id, fields="posts.limit(100).after(%s)" % (next_page))
                    else:
                        filter_stop = True
                        break
                
                # Take the last post because it is the end of all posts from the page
                # and not stop because of filter
                if not filter_stop:
                    posts += cursor["posts"]["data"]

                self.posts_list += posts
            except facebook.GraphAPIError:
                self.reinsert_access_token()

    def get_comments(self, verbose=False):
        if not hasattr(self, 'posts_list'):
            raise Exception("get_posts is not ran yet")

        posts = []
        for counter, post in enumerate(self.posts_list):
            try:
                post_id = post["id"]

                if verbose:
                    print("[%5d/%5d]" % (counter + 1, len(self.posts_list)), post_id)

                # Get first object cursor
                cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100)")
                comments = []

                if "comments" in cursor:
                    while "next" in cursor["comments"]["paging"]:
                        # Get next object cursor link
                        next_page = strip_next_page_token(cursor["comments"]["paging"]["next"])
                        _comments = cursor["comments"]["data"]

                        # L128-L131 Can be pythonized using map(func, col)
                        for _comment in _comments:
                            # Convert to UNIX time
                            _comment["created_time"] = int(parser.parse(_comment["created_time"]).timestamp())
                        comments += _comments

                        # Move to next object cursor
                        cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100).after(%s)" % (next_page))

                post["comments"] = comments
                posts.append(post)
            except facebook.GraphAPIError:
                self.reinsert_access_token()
        self.posts = posts

    def get_comments_count(self, verbose=False):
        if not hasattr(self, 'posts_list'):
            raise Exception("get_posts is not ran yet")
        
        posts = []
        counter = 1
        total_comment_count = 0
        for post in self.posts_list:
            try:
                post_id = post["id"]

                if verbose:
                    print("[%5d/%5d]" % (counter, len(self.posts_list)), post_id)
                    counter += 1

                # Get first object cursor
                cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100)")
                comment_count = 0
                post["comment_count"] = 0
                if "comments" in cursor:
                    while "next" in cursor["comments"]["paging"]:
                        # Get next object cursor link
                        next_page = strip_next_page_token(cursor["comments"]["paging"]["next"])

                        # Grab the comments (in list form)
                        _comments = cursor["comments"]["data"]

                        # Get the count of comments
                        comment_count += len(_comments)
                        print(comment_count)

                        # Move to next page
                        cursor = self.graph.get_object(id=post_id, fields="message,comments.limit(100).after(%s)" % (next_page))

                        # Add to master
                        post["comment_count"] = comment_count
                        total_comment_count += comment_count
                posts.append(post)
            except facebook.GraphAPIError:
                self.reinsert_access_token()
        self.posts = posts
        self.total_comment_count = total_comment_count

    def get_levelled_comments_count(self, verbose=False):
        if not hasattr(self, 'posts_list'):
            raise Exception("get_posts is not ran yet")

        counter = 1
        total_comment_count = 0
        total_nested_comment_count = 0

        for counter, post in enumerate(self.posts_list):
            try:
                post_id = post["id"]
                if verbose:
                    print("[%5d/%5d]" % (counter, len(self.posts_list)), end=' ')
                
                # Get first object cursor
                cursor = self.graph.get_object(id=post_id, fields="comments.limit(100){message,comment_count}")
            
                if "comments" in cursor:
                    total_comment_count += len(cursor["comments"]["data"])

                    # Loop through nested comments and get the total count
                    for comment in cursor["comments"]["data"]:
                        total_nested_comment_count += comment["comment_count"]
                        total_comment_count += comment["comment_count"]

                    # Will not run no next object cursor
                    while "next" in cursor["comments"]["paging"]:
                        # Get next object cursor link
                        next_page = strip_next_page_token(cursor["comments"]["paging"]["next"])
                        
                        # Move to next object cursor
                        cursor = self.graph.get_object(id=post_id, fields="comments.after(%s).limit(100){message, comment_count}" % (next_page))

                        # Sum top level comment count
                        total_comment_count += len(cursor["comments"]["data"])

                        # Loop through nested comments and get the total count
                        for comment in cursor["comments"]["data"]:
                            total_nested_comment_count += comment["comment_count"]
                            total_comment_count += comment["comment_count"]

                if verbose:
                    print("tcc: %8d   tncc: %8d" % (total_comment_count, total_nested_comment_count))
            except facebook.GraphAPIError as e:
                print(e)
                self.reinsert_access_token()
        self.total_comment_count = total_comment_count
        self.total_nested_comment_count = 0
        self.comment_count = {"Total comment count": total_comment_count, "Total nested comment count": total_nested_comment_count}
    
    def reinsert_access_token(self):
        """
        Notify user that access token had expired. Will appear through the official notification stream of the OS.
        """
        n = notify2.Notification("Access token expired")
        n.show()

        # Input new access token through console
        access_token = input("Access token expired. Please enter a new access token: ")
        self.graph.access_token = access_token
        self.access_token = access_token
        n.close()

