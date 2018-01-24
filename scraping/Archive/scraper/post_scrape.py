import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import datetime

global page_no
page_no = 0
#counter = 0

def post_scrape_main(link):
    main_link = "https://forum.lowyat.net"
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    try:
        page = urllib.request.urlopen(link)
    except:
        print("\t\t[P] Caught HTTPError, sleeping for 10 minutes.")
        time.sleep(600)
        try:
            page = urllib.request.urlopen(link)
        except:
            with open("data\scraperesults\lowyat\failed_links.txt", 'a') as f:
                for row in f:
                    f.write(link + '\n')
            return 0,0
    
    soup = bs(page, "lxml")
    #For debugging purposes, prints raw html to file
#    with open('temp.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
    
    [div.extract() for div in soup.find_all("div", { "class" : "quotemain"})]   #Removes quote text
    [div.extract() for div in soup.find_all("div", { "class" : "quotetop"})]    #Removes quote timestamp
    [div.extract() for div in soup.find_all("span", { "class" : "edit"})]       #Removes edit text and timestamps
    
    un_list = []
    time_list = []
    avatar_title = []
    info_group = []
    info_post_count = []
    info_joined = []
    info_from = []
    text = []
    
    usernames = soup.find_all("span", class_="normalname")
    for a in usernames:
        un_list.append(a.get_text())
        
    timestamp = soup.find_all("div", style="float: left;")
    for a in timestamp:
        try:
            time_string = a.find('span', class_='postdetails').get_text()
            time_string = time_string.split(',')[0]
            time_string = time_string.replace("Today",today.strftime("%b %d %Y")).replace("Yesterday",yesterday.strftime("%b %d %Y")).strip()
            time_string = time.strptime(time_string, "%b %d %Y")
            time_string = time.strftime("%Y%m%d", time_string)
            time_list.append(time_string)
        except AttributeError:
            pass
    
    userinfo = soup.find_all("table", class_="post_table")
    for a in userinfo:
        avatar_title.append(a.find("div", class_="avatar").get_text().strip())
        info_group.append(list(a.find("div", class_="avatar_extra").stripped_strings)[0])
        info_post_count.append(list(a.find("div", class_="avatar_extra").stripped_strings)[1])
        join_date_string = list(a.find("div", class_="avatar_extra").stripped_strings)[2].split(':')[1].strip()
        
        if ("Today" not in join_date_string) and ("Yesterday" not in join_date_string):
            join_date_string = time.strptime(join_date_string, "%b %Y")
            join_date_string = time.strftime("%Y%m", join_date_string)
        elif ("Today" in join_date_string):
            join_date_string = datetime.datetime.strftime(datetime.datetime.today(), "%Y%m")
        elif ("Yesterday" in join_date_string):
            join_date_string = datetime.datetime.strftime(datetime.datetime.today()-datetime.timedelta(1), "%Y%m")
            
        info_joined.append(join_date_string)
        
        try:
            info_from.append(list(a.find("div", class_="avatar_extra").stripped_strings)[3])
        except IndexError:
            info_from.append("")
            
        try:
            text.append(a.find("div", class_="postcolor post_text").get_text().strip())
        except:
            text.append("")
            
    try:
        np_link = main_link + soup.find("a", title="Next page")['href']
    except:
        np_link = 0
    
    index_set = list(zip(un_list,time_list,avatar_title,info_group,info_post_count,info_joined,info_from,text))
    df = pd.DataFrame(data = index_set, columns=['username','date','avatar_title','group','post_count','join_date','from','text'])
    return df, np_link

def post_scrape(link, page_limit=50, counter=0, verbose = False):
    global page_no
    page_no = 0
    frames = []
    
    while (True):
        if (counter == 45):
            print("\t\t[P] *****15 second delay initated to prevent forum block*****")
            time.sleep(15)
            counter = 0
        if (page_no == page_limit):
            return pd.concat(frames, ignore_index=True), counter
        page_no += 1
        counter += 1
        if page_no == 1:
            if verbose == True:
                print("\t\t[P] Page = " + str(page_no) + " Counter = " + str(counter) + " " + link)
            prev_link = link
            df, np_link = post_scrape_main(link)
            frames.append(df)
            if np_link == 0:
                if verbose == True:
                    print("\t\t[P] Last page reached at: " + prev_link)
                return pd.concat(frames, ignore_index=True), counter
        else:
            if verbose == True:
                print("\t\t[P] Page = " + str(page_no) + " Counter = " + str(counter) + " " + np_link)
            prev_link = np_link
            df, np_link = post_scrape_main(np_link)
            frames.append(df)
            if np_link == 0:
                if verbose == True:
                    print("\t\t[P] Last page reached at: " + prev_link)
                return pd.concat(frames, ignore_index=True), counter
            
#print(post_scrape("https://forum.lowyat.net/topic/4271549"))