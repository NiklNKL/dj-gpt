import time
import random
import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent

from config import *

def _rotate_tor_ip():
    try:
        with Controller.from_port(port=9051) as c:
            c.authenticate(password=None)  # oder cookie_path falls nötig
            c.signal(Signal.NEWNYM)
            print("🔄 Neue Tor-Identität angefordert")
    except Exception as e:
        print(f"⚠️ Fehler bei IP-Wechsel: {e}")

def _get_html(url):
    """
    Robust HTML-Scraper mit Tor, Random Delays, Headers und Block-Erkennung.
    """
    print(f"➡️ TOR-Request: {url}")
    for attempt in range(SCRAPE_RETRIES_AMOUNT):
        try:
            delay = random.uniform(SCRAPE_RTD_MINIMUM, SCRAPE_RTD_MAXIMUM)
            print(f"⏳ Warte {delay:.2f}s vor Request...")
            time.sleep(delay)

            _rotate_tor_ip()

            proxies = {'http': SCRAPE_PROXY, 'https': SCRAPE_PROXY}
            headers = {
                'User-Agent': (
                    UserAgent().chrome  # stabiler als `.random`
                ),
                'Referer': 'https://www.azlyrics.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate'
            }

            response = requests.get(url, proxies=proxies, headers=headers, timeout=10)

            if not response.ok or "blocked" in response.text.lower():
                raise Exception("🚫 Möglicher Block durch Server")

            print(f"✅ Erfolgreich geladen: {url}")
            return response.content

        except Exception as e:
            print(f"⚠️ Versuch {attempt+1} fehlgeschlagen: {e}")
            backoff = random.uniform(SCRAPE_RTD_ERROR_MINIMUM, SCRAPE_RTD_ERROR_MAXIMUM)
            print(f"🔁 Backoff {backoff:.2f}s...")
            time.sleep(backoff)

    print(f"❌ HTML konnte nicht geladen werden: {url}")
    return None
