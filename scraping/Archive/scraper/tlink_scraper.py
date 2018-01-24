import urllib
from bs4 import BeautifulSoup as bs
import time
#import pandas as pd
import datetime
import re

global page_no
global counter
page_no = 0
counter = 0

def tlink_scrape_main(link, sdate, edate, search_list=[]):
    main_link = "https://forum.lowyat.net"
    page = urllib.request.urlopen(link)
    soup = bs(page, "lxml")
    
#Initialize date variables
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(1)
    
    if (sdate.lower() == "today"):
        start_date = today
    elif (sdate.lower() == "yesterday"):
        start_date = yesterday
    else:
        start_date = datetime.datetime.strptime(sdate, "%Y%m%d")
        
    if (edate.lower() == "today"):
        end_date = today
    elif (edate.lower() == "yesterday"):
        end_date = yesterday
    else:
        end_date = datetime.datetime.strptime(edate, "%Y%m%d")
        
    if (start_date > end_date):
        raise ValueError("Invalid start-end date pairs, please redefine start-end dates.")
    
    #For debugging purposes, prints raw html to file
#    with open('temp.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
    
    titles = []
    desc = []
    tlink = []
    tdate_list = []
    
    topics = soup.find_all("td", class_="row1", valign="middle")
#    with open('temp2.html', 'wb') as f:
#        for a in topics:
#            f.write(a.prettify('utf8'))
    
    for a in topics:
        tdate = a.find("a")['title'][24:]
        if "Today" in tdate:
            tdate = tdate.replace("Today", datetime.datetime.strftime(today, "%b %d %Y"))
        elif "Yesterday" in tdate:
            tdate = tdate.replace("Yesterday", datetime.datetime.strftime(yesterday, "%b %d %Y"))
        tdate = datetime.datetime.strptime(tdate, "%b %d %Y, %I:%M %p")
        #if (sdate != "") and (edate != ""):
        date_test = start_date <= tdate <= end_date #Test date in range
        tdate = datetime.datetime.strftime(tdate, "%Y%m%dT%H%M%S")
        if search_list != []:
            if (sdate != "") or (edate != ""):
                if date_test == True:
                    for word in search_list:
                        try:
                            #if (word.lower() in list(a.stripped_strings)[0].lower()) or (word.lower() in list(a.stripped_strings)[5].lower()):
                            if (re.search(r'\b'+word.lower()+r'\b', list(a.stripped_strings)[0].lower()) or re.search(r'\b'+word.lower()+r'\b', list(a.stripped_strings)[5].lower())):
                                titles.append(list(a.stripped_strings)[0])
                                try:
                                    desc.append(list(a.stripped_strings)[5])
                                except:
                                    desc.append("")
                                tlink.append(main_link + a.find("a")['href'])
                                tdate_list.append(tdate)
                        except:
                            if re.search(r'\b'+word.lower()+r'\b', list(a.stripped_strings)[0].lower()):
                                titles.append(list(a.stripped_strings)[0])
                                try:
                                    desc.append(list(a.stripped_strings)[5])
                                except:
                                    desc.append("")
                                tlink.append(main_link + a.find("a")['href'])
                                tdate_list.append(tdate)
        elif (sdate != "") or (edate != ""):
            if date_test == True:
                titles.append(list(a.stripped_strings)[0])
                try:
                    desc.append(list(a.stripped_strings)[5])
                except:
                    desc.append("")
                tlink.append(main_link + a.find("a")['href'])
                tdate_list.append(tdate)
        else:
            titles.append(list(a.stripped_strings)[0])
            try:
                desc.append(list(a.stripped_strings)[5])
            except:
                desc.append("")
            tlink.append(main_link + a.find("a")['href'])
            tdate_list.append(tdate)
            
    try:
        np_link = main_link + soup.find("a", title="Next page")['href']
    except:
        np_link = 0
    
#    index_set = list(zip(titles,desc,tlink,tdate_list))
#    df = pd.DataFrame(data = index_set, columns=['titles','desc','link','date'])
#    df.to_csv('temp.csv',index=False)
    
    return tlink, np_link, titles, tdate_list

def tlink_scrape(link, sdate, edate, page_limit=50, search_list=[], verbose = False):
    global page_no
    global counter
    page_no = 0
    links_retrieved = []
    titles_retrieved = []
    tdate_retrieved = []
    
    while (True):
        if (counter == 45):
            print("\t[T] *****15 second delay initated to prevent forum block*****")
            time.sleep(15)
            counter = 0
        if (page_no == page_limit):
            return links_retrieved, titles_retrieved, tdate_retrieved, counter
        page_no += 1
        counter += 1
        if page_no == 1:
            if verbose == True:
                print("\t[T] Page = " + str(page_no) + " Counter = " + str(counter) + " " + link)
            prev_link = link
            tlink, np_link, titles, tdate_list = tlink_scrape_main(link,  sdate, edate, search_list)
            links_retrieved = links_retrieved + tlink
            titles_retrieved = titles_retrieved + titles
            tdate_retrieved = tdate_retrieved + tdate_list
            if np_link == 0:
                print("\tLast page reached at: " + prev_link)
                return links_retrieved, titles_retrieved, tdate_retrieved, counter
        else:
            if verbose == True:
                print("\t[T] Page = " + str(page_no) + " Counter = " + str(counter) + " " + np_link)
            prev_link = np_link
            tlink, np_link, titles, tdate_list= tlink_scrape_main(np_link, sdate, edate, search_list)
            links_retrieved = links_retrieved + tlink
            titles_retrieved = titles_retrieved + titles
            tdate_retrieved = tdate_retrieved + tdate_list
            if np_link == 0:
                if verbose == True:
                    print("\t[T] Last page reached at: " + prev_link)
                return links_retrieved, titles_retrieved, tdate_retrieved, counter
            
#print(tlink_scrape("https://forum.lowyat.net/Kopitiam", "yesterday", "today", 1))