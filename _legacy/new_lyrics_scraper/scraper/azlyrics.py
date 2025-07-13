from bs4 import BeautifulSoup
from . import string_cleaner
from tor_controller import _get_html
from config import AZ_LYRICS_BASE_URL

def get_artist_url_list(letter):
    url = f'{AZ_LYRICS_BASE_URL}/{letter}.html'
    html = _get_html(url)
    artist_urls = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for column in soup.find_all('div', class_='artist-col'):
            for a in column.find_all('a'):
                name = string_cleaner.clean_name(a.text)
                artist_url = string_cleaner.clean_url(f"{AZ_LYRICS_BASE_URL}/{a['href']}")
                artist_urls.append((name, artist_url))
    return artist_urls

def get_song_url_list(artist_url):
    html = _get_html(artist_url)
    song_urls = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find('div', id='listAlbum').find_all('a'):
            name = string_cleaner.clean_name(a.text)
            url = string_cleaner.clean_url(f"{AZ_LYRICS_BASE_URL}/{a['href'].replace('../', '')}")
            song_urls.append((name, url))
    return song_urls

def get_song_lyrics(song_url):
    html = _get_html(song_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        divs = [div.text for div in soup.find_all('div', class_=None)]
        if divs:
            lyrics = max(divs, key=len)
            return string_cleaner.clean_lyrics(lyrics)
    return ""
