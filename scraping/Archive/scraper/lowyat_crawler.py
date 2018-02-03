import urllib
from bs4 import BeautifulSoup as bs

def crawler(lin, search_list=[]):
    return None


def crawl_levels(link, n, l1_search, l2_search):
    merged_searches = l1_search + l2_search
    
    links = []
    for searches in merged_searches:
        new_link = link + searches
        print(new_link)
        links.append(new_link)
    return links