from bs4 import BeautifulSoup  
import http.client
import urllib
_current_page = 232
_total_page = 1
while _current_page != _total_page:
    _current_page += 1
    print("current page: ", _current_page)
    _get_url_checker1 = True
    while _get_url_checker1 == True:
        try:
            _sauce = urllib.request.urlopen('https://cforum1.cari.com.my/forum.php?mod=forumdisplay&fid=562&page=' + str(_current_page))
            _get_url_checker1 = False
        except urllib.error.HTTPError as _err:
            print('HTTP ERROR in page ' + str(_current_page) + ' when scraping the post address')
            print(_err.reason)
        except urllib.error.URLError as _err:
            print('URL ERROR in page ' + str(_current_page) + ' when scraping the post address')
            print(_err.reason)
            
    _get_page_soup = True
    while _get_page_soup == True:
        try:
            _soup = BeautifulSoup(_sauce, 'html.parser') 
            _get_page_soup = False
            
        except http.client.IncompleteRead as _err:
            _soup = _err.partial.decode('gbk')
            print('Error in line 31')
        except:
            pass
            
    #https://cforum1.cari.com.my/ 
    _a = _soup.find_all('a')
    for _item in _a:
        try:
            _total_page = _item['totalpage']
            print("total page:", _total_page)
        except:
            pass
        
    if _current_page == 1:
        _a_sxst_list = _soup.find_all('a', attrs={"class": "s xst"})[5:]
    else:
        _a_sxst_list = _soup.find_all('a', attrs={"class": "s xst"})
    
    _link_list = []
    for _b in _a_sxst_list:
        _link_list.append(['https://cforum1.cari.com.my/' + _b['href'] , _b.string.replace(',','')]) 
    
    for _link in _link_list:        
        if _link[0] == 'https://cforum1.cari.com.my/forum.php?mod=viewthread&tid=3936394&extra=page%3D233':         
            continue
        _current_section = 0
        _total_section = 1
        _list = [] 
        _data_list = [] 
        _find_total_section = True
        while _current_section != _total_section: 
            _current_section += 1
            _get_url_checker2 = True
            while _get_url_checker2 == True:
                try:
                    _sauce = urllib.request.urlopen(_link[0] + '&page=' + str(_current_section))
                    _get_url_checker2 = False
                except urllib.error.HTTPError as _err:
                    print('HTTP ERROR!!!!!!!!!')
                    print(_err.reason)
                    print(_link[0])
                except urllib.error.URLError as _err:
                    print('URL ERROR!!!!!!!!!!')
                    print(_err.reason)
                    
            print(_link[0] + '&page=' + str(_current_section))
            _get_section_soup = True
            try:
                while _get_section_soup:
                    try:
                        _soup = BeautifulSoup(_sauce, 'html.parser') 
                        _get_section_soup = False
                    except http.client.IncompleteRead as _err:
                        _soup = _err.partial.decode('gbk')
                    except:
                        print("BeautifulSoup error at line 82")
                        print(_link[0] + '&page=' + str(_current_section))
                        
                _span = _soup.find_all('span')
                while _find_total_section == True:
                    for _item in _span:
                        try:
                            _total_section = int(_item['title'].split()[1])
                            print("total section:", _total_section)  
                        except:
                            pass
                        _find_total_section = False
                        
                _em = _soup.find_all('em') 
                _a = _soup.find_all('a', attrs={"class": "xw1"}) 
                _counter = 0 
                
                #get id, date
                _date_checker = True #check for the posting date is 2017 forward
                for item in _em: 
                    try: 
                        _data_list.append([item['id'].replace('authorposton','postmessage_'), item.text.split()[1], _a[_counter].text])
                        _counter += 1
                        if _date_checker == True:
                            if _data_list[0][1].split('-')[2] != '2017':
                                _current_section = _total_section   
                                break
                            _date_checker = False
                    except: 
                        pass
                    
                #removing of non-related text
                for _em in _soup('em'):
                    _em.decompose()
                
                for _p in _soup('p'):
                    _p.decompose()
                    
                for _p in _soup('i'):
                    _p.decompose()
                
                for _blockquote in _soup('blockquote'):
                    _blockquote.decompose()
                    
                for _script in _soup('script'):
                    _script.decompose()  
                    
                for _fb_post in _soup('div', attrs={'class' : "fb-post"}):
                    _fb_post.decompose()   
                       
                #get text
                for _data in _data_list:
                    try:
                        _data.append(_soup.find('td', attrs={"id": _data[0]}).text)
                    except:
                        pass
                

            except http.client.IncompleteRead as _err: 
                #_soup = _err.partial 
                print(_err)
                
                #print(_link[0]) 
                #print(_soup.decode('gbk')) 
                #print('BOTTOM')  
                                #convert date to lowyat format
        for _data in _data_list: 
            try: 
                _temp_for_split = _data[1].split('-') 
                if len(_temp_for_split[0]) == 1: 
                    _temp_for_split[0] = '0' + _temp_for_split[0] 
                    
                if len(_temp_for_split[1]) == 1: 
                    _temp_for_split[1] = '0' + _temp_for_split[1] 
                    
                _data[1] = _temp_for_split[2] + _temp_for_split[1] + _temp_for_split[0] 
            except: 
                pass 
        try: 
            print( _data_list[0][1]) 
            if _data_list[0][1].startswith('2017') == True: 
                with open('data/scraperesults/carinet/carinet_' + _data_list[0][1] + '_' + _link[1].replace('?','').replace('，','').replace(',','').replace('~','').replace('#','').replace('%','').replace('&','').replace('*','').replace('/','').replace('\\','').replace('{','').replace('}','').replace(':','').replace('<','').replace('>','').replace('+','').replace('|','').replace('"','') + '.csv', 'w', encoding="UTF-8") as outFile:
                    outFile.write('Topic title: ')
                    outFile.write(_link[1])
                    outFile.write('\n')
                    outFile.write('username,date,text\n')
                    for _data in _data_list: 
                        print(_data)
                        try:
                            outFile.write(_data[2] + "," + _data[1] + "," + '"' + _data[3].replace('\n','').replace('\r','').replace('"','') + '"') 
                            outFile.write('\n')
                        except IndexError:
                            pass
        except IndexError:
            pass