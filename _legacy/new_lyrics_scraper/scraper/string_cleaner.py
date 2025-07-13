import re
import unidecode
from config import *

def clean_url(url): return url.lower().strip()
def clean_name(name): return unidecode.unidecode(name.lower().strip())
def clean_lyrics(lyrics):
    lyrics = unidecode.unidecode(lyrics.lower().strip())
    lyrics = re.sub(r'[(\[].*?[)\]]', '', lyrics)
    for _ in range(STR_CLEAN_TIMES):
        for old, new in STR_CLEAN_DICT.items():
            lyrics = lyrics.replace(old, new)
    return lyrics.strip()
