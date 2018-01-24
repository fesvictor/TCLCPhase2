import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import datetime

def scrape_page(link):
    
    list_of_lists = []
    
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = bs(page, "lxml")
    #For debugging purposes, prints raw html to file
#    with open('lks_temp.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
    
    try:
        next_page = soup.find("div", class_="navigation", id="pagenavi")
        next_page = next_page.a["href"]
    except:
        next_page = None
        
    post = soup.find_all("div", id=lambda x: x and x.startswith("post-"))
    
    for a in post:
        check_comment = a.find("p", class_="postcontrols").find("a").get_text()
        if (check_comment != "No Comments"):
            buffer_list = []
            buffer_list.append(a.find("a").get_text()) #Stores post title
            date = a.find("p").get_text().split(',')[-2].strip()
            date = time.strptime(date, "%d %B %Y")
            date = time.strftime("%Y%m%d", date)
            buffer_list.append(date)
            buffer_list.append(check_comment)
            comments = comment_scrape(a.find("p", class_="postcontrols").find("a")['href'])
            list_of_lists.append(buffer_list + comments)

            
    df = pd.DataFrame(list_of_lists)
    return df, next_page

            
def comment_scrape(link):
    print("Scraping comments from: <" + link[:70] + "....>")
    buffer_list = []
    
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = bs(page, "lxml")
    
    all_comments = soup.find_all("li", class_=lambda x: x and x.startswith("comment"))
    #For debugging purposes, prints raw html to file
#    with open('lks_temp2.html', 'wb') as f:
#        for a in all_comments:
#            f.write(a.prettify('utf8'))
    
    for a in all_comments:
        try:
            user_info = a.find("span", class_ = "info")
            if (user_info):
                username = user_info.b.get_text()
                date = user_info.get_text().split(',')[1][1:].split('-')[0].strip()
                time_ = user_info.get_text().split('-')[1][1:].strip()
                comment = a.find("div", class_="text")
                if (comment):
                    buffer_list.append("{" + username + "}{" + date + "}{" + time_ + "} " + comment.p.get_text())
        except:
            if (user_info):
                username = user_info.find("a", id=lambda x: x and x.startswith("comment")).get_text()
                date = user_info.get_text().split(',')[1][1:].split('-')[0].strip()
                time_ = user_info.get_text().split('-')[1][1:].strip()
                comment = a.find("div", class_="text")
                if (comment):
                    buffer_list.append("{" + username + "}{" + date + "}{" + time_ + "} " + comment.p.get_text())
    return buffer_list
    
def scrape(link, max_pages=50, file_name="wordpress.csv"):
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
    resultdf.to_csv(file_name, index=False, encoding='utf-8')
    print("Scraping process completed for " + str(max_pages) + " pages in " + str('{0:.3f}'.format(time.time() - start_time)) + " seconds")
        
current_timestamp = datetime.datetime.now()
current_timestamp = current_timestamp.strftime("%Y%m%d_%H%M%S")
scrape("https://blog.limkitsiang.com/", max_pages=24, file_name="data/scraperesults/blog/limkitsiang_"+current_timestamp+".csv")