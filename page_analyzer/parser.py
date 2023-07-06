from bs4 import BeautifulSoup
import requests


def parsing(url):
    req = requests.get(url)
    parsed_url = {}
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    if soup.h1:
        parsed_url['h1'] = soup.h1.string
    if soup.title:
        parsed_url['title'] = soup.title.string.strip()
    if soup.find(attrs={'name': 'description'}):
        parsed_url['description'] = (
                soup.find(attrs={'name': 'description'})['content'].strip()
                )
    return parsed_url
