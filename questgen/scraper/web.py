import requests
from bs4 import BeautifulSoup


def scrape(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html5lib")
    [s.extract() for s in soup(["iframe", "script", "pre", "svg", "style"])]
    print(soup.get_text())


# scrape("https://madewithml.com/courses/foundations/linear-regression/")
# scrape("https://browser.engineering/forms.html")
scrape("https://basicbiology.net/biology-101/introduction-to-cells")
