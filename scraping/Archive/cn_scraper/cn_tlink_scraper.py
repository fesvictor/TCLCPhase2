import urllib
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import datetime as dt

def tlink_scrape_main(link):
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = bs(page, "lxml")
    
    #For debugging purposes, prints raw html to file
#    with open('temp.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
        
    all_threads = soup.find_all("tbody", id=re.compile("^normalthread"))
#    with open('temp2.html', 'wb') as f:
#        for a in all_threads:
#            f.write(a.prettify('utf8'))

    thread_title_list = []
    thread_link_list = []
    thread_date_list = []
    
    for a in all_threads:
        thread_title = a.find('a', class_='xst', onclick='atarget(this)').get_text()
        thread_title_list.append(thread_title)
        thread_link = a.find('a', class_='xst', onclick='atarget(this)')['href']
        thread_link_list.append('http://www.jbtalks.cc/' + thread_link)
        _date = a.find('td', class_='by').find('em').find('span').get_text()
        _date = dt.datetime.strptime(_date, '%Y-%m-%d %I:%M %p')
        thread_date = dt.datetime.strftime(_date, '%Y%m%d')
        thread_date_list.append(thread_date)
        
    try:
        np_link = 'http://www.jbtalks.cc/' + soup.find("a", class_='nxt')['href']
    except:
        np_link = 0
        
    return thread_title_list, thread_link_list, thread_date_list, np_link
    
def tlink_scrape(link, page_limit):
    
    titles_retrieved = []
    links_retrieved = []
    dates_retrieved = []
    
    page_no = 0
    
    while(True):
        page_no += 1
        if page_no == 1:
            title, tlink, tdate, np_link = tlink_scrape_main(link)
            titles_retrieved = titles_retrieved + title
            links_retrieved = links_retrieved + tlink
            dates_retrieved = dates_retrieved + tdate
            if np_link == 0:
                return titles_retrieved, links_retrieved, dates_retrieved
        if page_no == page_limit:
            return titles_retrieved, links_retrieved, dates_retrieved
        else:
            title, tlink, tdate, np_link = tlink_scrape_main(np_link)
            titles_retrieved = titles_retrieved + title
            links_retrieved = links_retrieved + tlink
            dates_retrieved = dates_retrieved + tdate
            if np_link == 0:
                return titles_retrieved, links_retrieved, dates_retrieved
        
#print(post_scrape("http://www.jbtalks.cc/thread-1703549-1-2.html"))
    
#print(tlink_scrape('http://www.jbtalks.cc/forum-674-1.html', 3))