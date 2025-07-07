import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_lyrics_sync(title: str, artist: str) -> str:
    query = f"{title} {artist}".replace(" ", "%20")
    search_url = f"https://www.musixmatch.com/search/{query}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/134.0.0.0 Safari/537.36"
    )
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("referer=https://www.google.com/")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(search_url)
        driver.implicitly_wait(5)

        try:
            link_element = driver.find_element(By.XPATH, "//a[contains(@href, '/lyrics/')]")
        except Exception:
            raise Exception("Lyrics link not found on Musixmatch search results")

        lyrics_url = "https://www.musixmatch.com" + link_element.get_attribute("href")
        driver.get(lyrics_url)
        driver.implicitly_wait(5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        blocks = soup.select(".lyrics__content__ok")
        if not blocks:
            # Save debug file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            debug_dir = "debug_html"
            os.makedirs(debug_dir, exist_ok=True)
            filename = f"{debug_dir}/musixmatch_debug_{title}_{artist}_{timestamp}.html".replace(" ", "_")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            raise Exception(f"Lyrics content not found. HTML saved to {filename}")

        lyrics = "\n".join(block.get_text(strip=True) for block in blocks)
        return lyrics.strip()

    finally:
        driver.quit()
