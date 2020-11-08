from bs4 import BeautifulSoup as bs
import requests
from requests_html import HTMLSession


def getAuthor(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        soup = bs(response.text, 'html.parser')
        if response.status_code == 200:
            meta = soup.find_all("meta")
            for tag in meta:
                if tag.get("name") == "author.name":
                    print(tag.get("content"))
    except requests.exceptions.RequestException as e:
        print(e)


#url='https://www.nytimes.com/2020/11/07/us/politics/biden-election.html'
url ='https://www.sfchronicle.com/health/article/Coronavirus-cases-are-rising-again-in-the-Bay-15708994.php'

getAuthor(url)