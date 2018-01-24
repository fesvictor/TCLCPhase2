import urllib
from bs4 import BeautifulSoup as bs
import time
import datetime
import pandas as pd

def scrape_page(link):
    list_of_lists = []
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = bs(page, "lxml")
    #For debugging purposes, prints raw html to file
#    with open('rkb_temp.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
        
    posts = soup.find_all("div", class_="date-outer")
    #For debugging purposes, prints raw html to file
#    with open('rkb_temp2.html', 'wb') as f:
#        for a in posts:
#            f.write(a.prettify('utf8'))
    try:
        next_page = soup.find("a", class_="blog-pager-older-link")["href"]
    except:
        next_page = None
        
    for a in posts:
        check_comment = a.find("span", class_="post-comment-link").a.get_text().strip()
        if (check_comment != "No comments:"):
            buffer_list = []
            buffer_list.append(a.find("h3", class_="post-title entry-title").get_text().strip()) #Stores post title
            date_ = a.find("h2", class_="date-header").get_text().split(",")
            date_ = date_[1].strip() + date_[2]
            date_ = time.strptime(date_, "%B %d %Y")
            date_ = time.strftime("%Y%m%d", date_)
            buffer_list.append(date_)
            buffer_list.append(check_comment[:-1])
            comments = comment_scrape(a.find("span", class_="post-comment-link").a["href"])
            list_of_lists.append(buffer_list + comments)
    df = pd.DataFrame(list_of_lists)
    return df, next_page
                    
def comment_scrape(link):
    print("Scraping comments from: <" + link[:70] + "....>")
    buffer_list = []
    username_list = []
    comment_list = []
    
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = bs(page, "lxml")
    
    all_comments = soup.find_all("p", class_=None)
    all_usernames = soup.find_all("span", dir="ltr")
    
    for a in all_usernames:
        try:
            username = a.get_text()
            if(username):
                username_list.append(username)
        except:
            pass
    for a in all_comments:
        try:
            comment = a.get_text()
            if(comment):
                comment_list.append(comment)
        except:
            pass
    
    for a in range(0,len(username_list)):
        buffer_list.append("{"+username_list[a]+"} "+comment_list[a])
    return buffer_list

def scrape(link, max_pages=50, file_name="blogspot.csv"):
    start_time = time.time()
    list_of_frames = []
    print("Scraping page 1 at: <" + link + ">")
    df, next_page = scrape_page(link)
    list_of_frames.append(df)
    for x in range(2,max_pages+1):
        print("Scraping page " + str(x) + " at: <" + next_page + ">")
        df, next_page = scrape_page(next_page)
        list_of_frames.append(df)
    resultdf = pd.concat(list_of_frames)
    resultdf = resultdf.add_prefix("column")
    resultdf.to_csv(file_name, index=False)
    print("Scraping process completed for " + str(max_pages) + " pages in " + str('{0:.3f}'.format(time.time() - start_time)) + " seconds")

current_timestamp = datetime.datetime.now()
current_timestamp = current_timestamp.strftime("%Y%m%d_%H%M%S")
#scrape("http://kadirjasin.blogspot.my/", max_pages=11, file_name="data/scraperesults/blog/kadirjasin_"+current_timestamp+".csv")
scrape("http://www.rockybru.com.my/", max_pages=17, file_name="data/scraperesults/blog/rockybru_"+current_timestamp+".csv")
