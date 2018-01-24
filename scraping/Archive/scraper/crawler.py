import urllib
from bs4 import BeautifulSoup as bs
#import pandas as pd

def crawler(link, search_list=[]):
    main_link = "https://forum.lowyat.net" 
    try:
        page = urllib.request.urlopen(link)
    except:
        return
    
    soup = bs(page, "lxml")
    
    #For debugging purposes, prints raw html to file
#    with open('level1_raw_html.html', 'wb') as f:
#        f.write(soup.prettify('utf8'))
    
    [div.extract() for div in soup.find_all("td", { "align" : "center"})]
    
    try:
        soup.find('div', id="fo_stat").decompose()
    except AttributeError:
        pass
    
    try:
        soup.find('div', id="forum_topic_list").decompose()
    except AttributeError:
        pass

    td = soup.find_all("td", class_="row2")
    href = []
    title = []
    result_list = []
    for b in td:
        href.append(main_link+b.find("b").findNext("a")['href']) #Reconstruct link from href
        title.append(b.find("b").findNext("a").get_text().strip('"'))
        
    index_set = list(zip(title,href))
    
    #Create CSV for debugging
#    l1_df = pd.DataFrame(data = index_set, columns=['topic','link'])
#    l1_df.to_csv('level1.csv',index=False)
    
    for i in range(0,len(index_set)):
        if search_list != []:
            for word in search_list:
                if word.lower() in index_set[i][0].lower():
                    result_list.append(index_set[i][1])
        else:
            result_list.append(index_set[i][1])
    return result_list

def crawl_levels(link, n, l1_search, l2_search):
    crawls = 1
    level1 = crawler(link, l1_search)
    links_retrieved = level1
    crawls += 1
    if (crawls <= n):
        for l in level1:
            try:
                links_retrieved = links_retrieved + crawler(l, l2_search)
            except:
                pass
    print("[C] Crawler retrieved links: " + str(links_retrieved))
    return links_retrieved