#Output csv files will be saved into "\data\scraperesults\lowyat"

import scraper.crawler as c
import scraper.tlink_scraper as t
import scraper.post_scrape as p
import read_wordlist as wl
from ReadParameterFile import get_parameter_dict
import datetime
import re
import pandas as pds

#Timestamp
start_time = datetime.datetime.now()

#List initialization
links_retrieved = []
titles = []
dates = []
pd = get_parameter_dict()
save_dir = pd['lowyat.files'].strip('./')+'/'

#Read word list
search_list = wl.read_wordlist()

#************CONFIGURATION******************
#CRAWLER CONFIG
link = pd['scraper.c.link'] #Start link
levels = int(pd['scraper.c.levels']) #Currently limited to 2 levels
l1_search = pd['scraper.c.l1_search'].split(',') #Level 1 filter (/Kopitiam)
l2_search = pd['scraper.c.l2_search'].split(',') #Level 2 filter (/Kopitiam/SeriousKopitiam)

#THREAD LINK scraper CONFIG
page_limit = 1750 #Default 50
#search_list = pd['scraper.t.search_list'].split(',')
start_date = "20170101" #Format = yyyymmdd
end_date = "today"
t_verbose = True

#POST scraper CONFIG
page_limit_p = 999999 #Default 50
p_verbose = False
#************CONFIGURATION END******************

#CRAWLER
print ("[C] Crawler task started for " + str(levels) + " level(s) for keywords " + str(l1_search) + " at L1, " + str(l2_search) + " at L2.")
link_list = c.crawl_levels(link, levels, l1_search, l2_search)
print("[C] Crawler task completed")

#THREAD LINK scraper
print("\t[T] Link scraper initiated with " + str(len(search_list)) + " keywords. With page limit: " + str(page_limit))
for l in link_list:
    print("\t[T] Link scraper task started for link: " + l)
    temp_retrieved, temp_titles, temp_date, counter = t.tlink_scrape(l, start_date, end_date, page_limit, search_list, t_verbose)
    links_retrieved = links_retrieved + temp_retrieved
    titles = titles + temp_titles
    dates = dates + temp_date
print("\t[T] Link scraper found total links: " + str(len(links_retrieved)))
print("\t[T] Link scraper task completed")


##Output to a file:
list_of_list = list(zip(links_retrieved, titles, dates))
tdf = pds.DataFrame(data = list_of_list, columns=['links_retrieved','title','dates'])
tdf.to_csv("data\scraperesults\lowyat\links_retrieved.csv", header=True, index=False)

##Use list
#counter = 0
#with open("data\scraperesults\lowyat\links_retrieved.txt", 'r') as f:
#    for row in f:
#        links_retrieved.append(row.strip())
#
#links_retrieved = links_retrieved[1721::]

#POST scraper
count = 0
print("\t\t[P] Post scraper initiated with page limit: " + str(page_limit_p))
for l,ttl,d in zip(links_retrieved, titles, dates):
    count += 1
    print("\t\t[P] Post scraper task started for link: " + str(l) + " (" + str(count) + "/" + str(len(links_retrieved)) + ")")
    df, counter = p.post_scrape(l, page_limit_p, counter, p_verbose)
    
    title_regex = re.sub(r'[^\w]', ' ', ttl)
    topic_number = l.split("https://forum.lowyat.net/topic/")[1]
    d_dt = datetime.datetime.strptime(d, "%Y%m%dT%H%M%S")
    
    file_name = "lowyat_" + datetime.datetime.strftime(d_dt, "%Y%m%d") + "_" + topic_number + "_" + title_regex + ".csv"
    full_filepath = save_dir + file_name
    try:
        with open(full_filepath, 'w') as f:
            current_timestamp = datetime.datetime.now()
            current_timestamp = current_timestamp.strftime("%d %b %Y, %H:%M:%S")
            
            try:
                f.writelines("Topic title: " + title_regex + ",")
            except:
                f.writelines("Topic title: " + ",")
                
            f.writelines("\"Topic posted on: " + datetime.datetime.strftime(d_dt, "%d %b %Y, %H:%M:%S") + "\",")
            f.writelines("Topic link: " + l + ",")
            f.writelines("\"Topic scraped on: " + current_timestamp + "\",")
            f.writelines("\n")
    except:
        file_name = "lowyat_" + datetime.datetime.strftime(d_dt, "%Y%m%d") + "_" + topic_number + "_" + ".csv"
        full_filepath = save_dir + file_name
        with open(full_filepath, 'w') as f:
            current_timestamp = datetime.datetime.now()
            current_timestamp = current_timestamp.strftime("%d %b %Y, %H:%M:%S")
            
            try:
                f.writelines("Topic title: " + title_regex + ",")
            except:
                f.writelines("Topic title: " + ",")
                
            f.writelines("\"Topic posted on: " + datetime.datetime.strftime(d_dt, "%d %b %Y, %H:%M:%S") + "\",")
            f.writelines("Topic link: " + l + ",")
            f.writelines("\"Topic scraped on: " + current_timestamp + "\",")
            f.writelines("\n")
    df.to_csv(full_filepath, header=True, index=False, mode='a')
print("\t\t[P] Post scraper task completed")

end_time = datetime.datetime.now()
total_time = end_time - start_time
total_time = str(total_time).split('.')[0]
total_time = str(total_time).split(':')
tt_h = total_time[0]+"h "
tt_m = total_time[1]+"m "
tt_s = total_time[2]+"s "
total_time = tt_h + tt_m + tt_s

print("Scraping process completed in " + total_time)