import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def format_to_azlyrics_url(artist, title):
    artist = re.sub(r"[^a-z0-9]", "", artist.lower())
    title = re.sub(r"[^a-z0-9]", "", title.lower())
    return f"https://www.azlyrics.com/lyrics/{artist}/{title}.html"

def get_lyrics_from_azlyrics(artist, title):
    url = format_to_azlyrics_url(artist, title)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None, f"Fehler: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all("div", class_=None, id=None)

        for div in divs:
            if div.text.strip():
                lyrics = div.get_text(separator="\n").strip()
                return lyrics, None
        return None, "Lyrics nicht gefunden."
    except Exception as e:
        return None, str(e)
