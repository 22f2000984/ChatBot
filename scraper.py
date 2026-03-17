import requests
from bs4 import BeautifulSoup

def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for s in soup(["script", "style"]):
        s.decompose()

    return soup.get_text(separator=" ")