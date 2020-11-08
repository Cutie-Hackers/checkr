from flask import Flask, render_template, request, redirect, session
from flask import render_template_string
from flask.helpers import url_for
import secrets
import urllib.parse

import urllib.request,sys,time
from bs4 import BeautifulSoup as bs
import requests
from requests_html import HTMLSession

app = Flask(__name__)
app.config["SECRET_KEY"] = "Sf3cput8zbVWkj1OUk5Wtg"

# flask development like this is called server side rendering (SSR)
# other type is client side rendering

# this means when i navigate to the '/' directory it will execute the hellow wolrd function and return that in the browser
@app.route('/main', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/info', methods=["GET", "POST"])
def info():
    url = request.form.get('url_input')
    data = getInfo(url)
    session["data"] = data
    return redirect( url_for('generic') )

@app.route('/generic', methods=["GET", "POST"])
def generic():
    data = session["data"]
    
    return render_template('generic.html', authors=data["authors"], title=data["title"], date=data["date"])


def getInfo(url):
    data = scrapper(url)
    data["url"] = url
    #data["score"] = date_relevance(data)
    return data

#----------------------------------------------------------------------------------------------------------------------#

#Access Website
#Score Indicator
vTitle = 0
vAuthor = 0
vDate = 0

def scrapper(url):
    session = HTMLSession()
    response = session.get(url)
    soup = bs(response.text, 'html.parser')

    #Title
    TITLE = soup.title.string
    if len(TITLE) > 1:
        vTitle = 20
    AUTHORS = []
    DATE = []
    #Author
    try:
        if response.status_code == 200:
            meta = soup.find_all("meta")
            for tag in meta:
                #print(tag)
                if tag.get("name") == "author.name":
                    AUTHORS.append((tag.get("content")))
                    vAuthor = 50
                if tag.get("name") == "byl":
                    AUTHORS.append((tag.get("content")))
                    vAuthor = 50
                if (tag.get("property") == "article:author") and tag.get("content") != 'https://www.facebook.com/SFChronicle/':
                    AUTHORS.append(tag.get("content")[31:].replace('-',' '))
                    vAuthor = 50
            a = soup.find_all("a")
            for tag in a:
                if tag.get("href") == "#noop":
                    AUTHORS.append((tag.get("class")))
                    vAuthor = 50

    except requests.exceptions.RequestException as e:
        return(e)


    #Time
    try:

        if response.status_code == 200:
            meta = soup.find_all("meta")
            for tag in meta:
                if tag.get("property") == "article:published_time":
                    DATE.append((tag.get("content")[:10]))
                    vDate = 30
                if tag.get("property") == "article:published":
                    DATE.append((tag.get("content")[:10]))
                    vDate = 30
    except requests.exceptions.RequestException as e:
        return(e)
    data = {
        "authors": AUTHORS,
        "date": DATE,
        "title": TITLE,
    }
    return data

# def date_relevance(data, article_score = (vTitle+vAuthor+vDate)):
#     current_year = 2020
#     article_year = int(data['date'][0:4])
#     score = article_score - 10*(current_year - article_year)
#     return(score)

