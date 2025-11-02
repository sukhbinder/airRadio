import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import os

url = "https://www.newsonair.gov.in/daily-broadcast/"


def get_direct_mp3_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    mp3_links = set()

    for tag in soup.find_all(["a", "audio"], href=True):
        candidate = tag.get("href")

        # decode encoded URLs (%2F etc.)
        candidate = unquote(candidate)

        # Look for real mp3 URLs on AIR domain
        match = re.search(r"https://www\.newsonair\.gov\.in[^\s\"']+\.mp3", candidate)
        if match:
            mp3_links.add(match.group())

    return sorted(mp3_links)


def download_mp3(url, folder="/tmp/mp3s"):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, url.split("/")[-1])

    try:
        print(f"Downloading: {url}")
        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved to {filename}")
    except Exception as e:
        print(f"Failed: {url} — {e}")


if __name__ == "__main__":
    links = get_direct_mp3_links(url)

    for link in links:
        if link.startswith("https://www.newsonair.gov.in/wp-content"):
            download_mp3(link)

