import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path
from time import sleep
from tqdm import tqdm

DB_PATH = Path("lyrics_db.jsonl")
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_billboard_top100():
    url = "https://www.billboard.com/charts/hot-100/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    chart_items = soup.select("li.o-chart-results-list__item h3")

    titles = [item.get_text(strip=True) for item in chart_items if item.get_text(strip=True)]
    artists = [a.get_text(strip=True) for a in soup.select("span.c-label.a-no-trucate")]

    return list(zip(artists, titles))[:100]  # Top 100

def format_to_azlyrics_url(artist, title):
    artist = re.sub(r"[^a-zA-Z0-9]", "", artist.lower())
    title = re.sub(r"[^a-zA-Z0-9]", "", title.lower())
    return f"https://www.azlyrics.com/lyrics/{artist}/{title}.html"

def extract_lyrics_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", class_=False, id=False)
    for div in divs:
        if div.text.strip() and len(div.text.strip().split("\n")) > 5:
            return div.get_text(separator="\n").strip()
    return None

def scrape_lyrics(artist, title):
    url = format_to_azlyrics_url(artist, title)
    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            return None
        lyrics = extract_lyrics_from_html(res.text)
        return {"artist": artist, "title": title, "lyrics": lyrics, "url": url} if lyrics else None
    except Exception as e:
        print(f"Fehler bei {artist} - {title}: {e}")
        return None

def save_entry(entry):
    with open(DB_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    DB_PATH.parent.mkdir(exist_ok=True)
    print("🎵 Lade Top-Songs von Billboard...")
    songs = get_billboard_top100()
    print(f"🔍 {len(songs)} Songs gefunden. Starte Scraping...")

    for artist, title in tqdm(songs, desc="Lyrics sammeln"):
        entry = scrape_lyrics(artist, title)
        if entry:
            save_entry(entry)
            sleep(1.5)
        else:
            print(f"❌ Keine Lyrics gefunden für: {artist} - {title}")

if __name__ == "__main__":
    main()
