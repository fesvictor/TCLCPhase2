import urllib
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

def post_scrape_main(link):
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = bs(page, "lxml")
    
    #For debugging purposes, prints raw html to file
#    with open('temp.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
        
    all_post = soup.find_all("div", id=re.compile("^post_\d+"))
#    with open('temp2.html', 'wb') as f:
#        for a in all_post:
#            f.write(a.prettify('utf8'))
    
    name_list = []
    date_posted_list = []
    post_content_list = []
    
    for a in all_post:
        name = a.find('a', class_='xw1', target='_blank').get_text()
        name_list.append(name)
        date_posted = a.find('em', id=re.compile("^authorposton")).get_text()[4:]
        date_posted_list.append(date_posted)
        try:
            post_content = a.find('td', class_='t_f', id=re.compile('^postmessage_')).get_text().strip()
            post_content_list.append(post_content)
        except:
            pass
        
    index_set = list(zip(name_list, date_posted_list, post_content_list))
    df = pd.DataFrame(data = index_set, columns=['username','date','text'])
    
    try:
        np_link = 'http://www.jbtalks.cc/' + soup.find("a", class_='nxt')['href']
    except:
        np_link = 0
            
    return df, np_link

def post_scrape(link):
    frames = []
    page_no = 0
    
    while(True):
        page_no += 1
        if page_no == 1:
            df, np_link = post_scrape_main(link)
            frames.append(df)
            if np_link == 0:
                return pd.concat(frames, ignore_index=True)
        else:
            df, np_link = post_scrape_main(np_link)
            frames.append(df)
            if np_link == 0:
                return pd.concat(frames, ignore_index=True)
        
#print(post_scrape("http://www.jbtalks.cc/thread-1703549-1-2.html"))