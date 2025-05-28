import streamlit as st
from scraper.azlyrics_scraper import get_lyrics_from_azlyrics

st.set_page_config(page_title="Live Song Scraper", layout="centered")

st.title("🎤 Live Song Lyrics Scraper")

with st.form("song_form"):
    artist = st.text_input("Künstlername", placeholder="z. B. Adele")
    title = st.text_input("Songtitel", placeholder="z. B. Hello")
    submitted = st.form_submit_button("Lyrics abrufen")

if submitted:
    if artist and title:
        with st.spinner("Scraping läuft..."):
            lyrics, error = get_lyrics_from_azlyrics(artist, title)
        if lyrics:
            st.success("Lyrics erfolgreich geladen!")
            st.text_area("Songtext", lyrics, height=400)
        else:
            st.error(f"Konnte keine Lyrics finden: {error}")
    else:
        st.warning("Bitte fülle beide Felder aus.")
