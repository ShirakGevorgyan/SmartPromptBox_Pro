import requests
from bs4 import BeautifulSoup

def fetch_lyrics_from_genius(title: str, artist: str) -> str:
    try:
        query = f"{title} {artist} site:genius.com"
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        genius_url = None
        for a in soup.find_all("a"):
            href = a.get("href")
            if href and "genius.com" in href and "/lyrics" in href:
                genius_url = href.split("&")[0].replace("/url?q=", "")
                break

        if not genius_url:
            return "Lyrics link not found on Google results."

        response = requests.get(genius_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        lyrics_blocks = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-6")
        if not lyrics_blocks:
            return "Lyrics block not found on Genius page."

        lyrics = "\n\n".join(block.get_text(separator="\n").strip() for block in lyrics_blocks)
        return lyrics or "Lyrics not found."
    
    except Exception as e:
        return f"Error scraping lyrics: {str(e)}"
