# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 03:18:39 2017

@author: Gary
"""

import cn_scraper.cn_tlink_scraper as t
import cn_scraper.cn_post_scraper as p
import re

titles_retreived = []
links_retrieved = []
dates_retrieved = []

page_limit = 3  

#THREAD LINK scraper
print("[T] Link scraper initiated with page limit: " + str(page_limit))
_titles, _links, _dates = t.tlink_scrape('http://www.jbtalks.cc/forum-674-1.html', page_limit)
titles_retreived = titles_retreived + _titles
links_retrieved = links_retrieved + _links
dates_retrieved = dates_retrieved + _dates
print("[T] Link scraper found total links: " + str(len(links_retrieved)))
print("[T] Link scraper task completed")

#POST scraper
count = 0
print("\t[P] Post scraper initiated.")
for ttl,l,d in zip(titles_retreived, links_retrieved, dates_retrieved):
    count += 1
    print("\t\t[P] Post scraper task started for link: " + str(l) + " (" + str(count) + "/" + str(len(links_retrieved)) + ")")
    df = p.post_scrape(l)
    title_regex = re.sub(r'[^\w]', ' ', ttl)
    file_name = "jbtalks_" + d + "_" + title_regex + ".csv"
    full_filepath = 'data/scraperesults/chinese/jbtalks/' + file_name
    df.to_csv(full_filepath, header=True, index=False, mode='a', encoding='utf-8')
print("\t\t[P] Post scraper task completed")