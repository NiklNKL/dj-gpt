import os
import csv
from config import CSV_FILE_DIR

def ensure_dir_exists():
    os.makedirs(CSV_FILE_DIR, exist_ok=True)

def song_exists(letter, artist_url, song_url):
    path = os.path.join(CSV_FILE_DIR, f"{letter}.csv")
    if os.path.isfile(path):
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            return any(row['artist_url'] == artist_url and row['song_url'] == song_url for row in reader)
    return False

def append_song(letter, artist, artist_url, song, song_url, lyrics):
    if not lyrics: return
    ensure_dir_exists()
    path = os.path.join(CSV_FILE_DIR, f"{letter}.csv")
    file_exists = os.path.isfile(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['artist', 'artist_url', 'song', 'song_url', 'lyrics'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'artist': artist,
            'artist_url': artist_url,
            'song': song,
            'song_url': song_url,
            'lyrics': lyrics
        })
