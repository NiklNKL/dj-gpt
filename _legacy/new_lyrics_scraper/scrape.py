from scraper import azlyrics, csv_writer

def scrape_letter(letter):
    artists = azlyrics.get_artist_url_list(letter)
    for artist, artist_url in artists:
        songs = azlyrics.get_song_url_list(artist_url)
        for song, song_url in songs:
            if not csv_writer.song_exists(letter, artist_url, song_url):
                lyrics = azlyrics.get_song_lyrics(song_url)
                csv_writer.append_song(letter, artist, artist_url, song, song_url, lyrics)
