
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

__author__ = "Partha Das"
__version__ = "1.0.2"

def getInfo(url):
    parsed = urlparse(url)
    try:
        html = urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        if soup.title is not None:
            title = soup.title.string
        else:
            title = 'N/A'
        return [parsed.netloc, title]
    except Exception as e:
        return ["", ""]

if __name__ == '__main__':
    print(getInfo('http://www.kjevik.dk/oddv/ViscountBMA.jpg'))
    print(getInfo('http://de.fishki.net/picsw/042008/28/googlefiles/032_googlefiles.jpg)'))

