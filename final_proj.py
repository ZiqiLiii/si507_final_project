#################################
##### Name: Ziqi Li
##### Uniqname: liziqi
#################################

from bs4 import BeautifulSoup
import requests
import json
from requests_oauthlib import OAuth1
import secrets

###############################################
######### Setting for using Cache #############
###############################################

CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}

def load_cache(): 
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache): 
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): 
        print("Using cache")
        return cache[url]     
    else:
        print("Fetching")
        response = requests.get(url) 
        cache[url] = response.text 
        save_cache(cache)          
        return cache[url]          

CACHE_DICT = load_cache()


#####################################################
#### Scraping a new single page - From Billboard ####
#####################################################

def build_song_list():
    ''' Make a list that include songs info from "https://www.billboard.com/charts/hot-100"

    Parameters
    ----------
    None

    Returns
    -------
    list include the rank, name and artist of the top 100 songs
    '''
    song_name_list=[]
    song_artist_list=[]
    song_rank_list=[]
    song_list=[]
    url="https://www.billboard.com/charts/hot-100"
    html_text = make_url_request_using_cache(url, CACHE_DICT)
    soup = BeautifulSoup(html_text, 'html.parser')
    all_list_name = soup.find_all('span',class_="chart-element__information__song text--truncate color--primary")
    all_list_artist = soup.find_all('span',class_="chart-element__information__artist text--truncate color--secondary")
    all_list_rank = soup.find_all('span',class_="chart-element__rank__number")
    # can include peak rank and the number of weeks of staying at the board if we want to get more records#
    for i in all_list_name:
        name = i.text
        song_name_list.append(name)
    for i in all_list_artist:
        artist = i.text
        song_artist_list.append(artist)
    for i in all_list_rank:
        rank = i.text
        song_rank_list.append(rank)
    for x in range(0,100):
        item = "Rank{} {} by {}".format(song_rank_list[x],song_name_list[x],song_artist_list[x])
        song_list.append(item)
    print(song_list)

build_song_list()


################################################
#### Access the Web API  - From Spotify API ####
################################################