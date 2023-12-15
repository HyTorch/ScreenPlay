# packages we want to include
import requests
import re
import string
import json
from credentials import *
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#uses webdriver object 
def get_js_soup(url,browser):
    try:
        browser.get(url)
        res_html = browser.execute_script('return document.body.innerHTML')
        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
        return soup
    except:
        return None

#extracts all alphabetical urls from the directory
def scrape_dir_page(dir_url, browser):
    print ('-'*20,'Scraping movies','-'*20)
    movie_links = []
    movie_titles = []
    meta_links = []
    movie_base_url = 'https://www.imsdb.com/scripts/' 
    meta_base_url = 'https://www.imsdb.com/Movie Scripts/'
    
    #execute js on webpage to load faculty listings on webpage and get ready to parse the loaded HTML 
    soup = get_js_soup(dir_url, browser)
    if soup == None:
        return None
    
    for link in soup.find_all(valign='top'):
        child = link.find_all('p')
        for script in child:
            # lots of quirky formatting issues, kind of mcguyvered this part lel
            title = script.find('a')['href'][15:-12]
            movie_titles.append(title)
            script_url = title.replace(' ', '-') + '.html'
            meta_links.append((meta_base_url + title + ' Script.html').replace(' ', '%20'))
            movie_links.append(movie_base_url + script_url)
                
    print ('-'*20,'Found {} movie urls'.format(len(movie_links)),'-'*20)
    print(movie_titles)
    return movie_links, movie_titles, meta_links

def make_dict(script):
    formatAndSplit = re.sub(r'[^A-Za-z]', ' ', script).lower().split()
    wordfreq = {}
    for raw_word in formatAndSplit:
        if raw_word not in wordfreq:
            wordfreq[raw_word] = 0
        wordfreq[raw_word] += 1
    return wordfreq

def get_movie_script(link):
    soup = get_js_soup(link, browser)
    try:
        script = soup.pre.get_text(strip=True)

        return make_dict(script)
    except:
        return None

def getMetaTuple(link, browser):
    soup = get_js_soup(link, browser)
    info = soup.find('table', class_='script-details')

    if info is None:
        return None

    rating = None
    releaseDate = None
    moviePic = None
    genreList = []

    try:
        ratingSoup = str(info.find('b', text='Average user rating').next_sibling.next_sibling.next_sibling.next_sibling).strip()
        rating = ratingSoup[ratingSoup.index('(') + 1:ratingSoup.index(' ')]
    except:
        pass

    try:
        releaseDateSoup = str(info.find('b', text='Script Date').next_sibling)
        releaseDate = releaseDateSoup[releaseDateSoup.index(':') + 1:].strip()
    except:
        pass
    
    moviePic = info.find('img')['src']

    genre = info.find('b', text='Genres').next_sibling.next_sibling.next_sibling
    while str(genre).startswith("<a href=\"/genre/"):
        soupString = str(genre)
        genreList.append(soupString[16:soupString.index('\"', 16)])
        genre = genre.next_sibling.next_sibling.next_sibling


    return ((rating, releaseDate, moviePic, genreList))

def save_dict_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)

if __name__ == "__main__":
    options = Options()
    options.add_experimental_option("detach",True)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)

    base_url = 'https://www.imsdb.com/alphabetical/'
    # driver.get(base_url)
    alpha_d = ['0'] + list(string.ascii_uppercase)
    total_movie_links = []
    total_titles = []
    total_metas = []
    for l in alpha_d:
        print("Page: ", base_url + l)
        links, titles, metas = scrape_dir_page(base_url + l, browser)
        print("Links: ", links)
        if links != None:
            total_movie_links.extend(links)
            total_titles.extend(titles)
            total_metas.extend(metas)
    print("Total Number of Scripts : " + str(len(total_movie_links)))


    script_dicts = []
    title_list = []
    meta_list = []
    for idx, link in enumerate(total_movie_links):
        script_dict = get_movie_script(link)
        if script_dict != None:
            print("got script dict ", idx)
            title_list.append((total_titles[idx], sum(script_dict.values())))
            script_dicts.append(script_dict)
            meta_list.append(getMetaTuple(total_metas[idx], browser))


    #code to create df dictionary
    df_dict = dict()
    for script_dict in script_dicts:
        for word in script_dict.keys():
            if word not in df_dict:
                df_dict[word] = 0
            df_dict[word] += 1

    # Save dictionaries locally
    save_dict_to_file(script_dicts, 'movieWords.json') # total count of each words of each movie scripts
    save_dict_to_file(title_list, 'titleList.json') # total amount of words of each movie's scripts
    save_dict_to_file(meta_list, 'metaList.json') # just meta data
    save_dict_to_file(df_dict, 'dfDict.json') # total count of words of all movie scripts

    print("Data saved locally.")