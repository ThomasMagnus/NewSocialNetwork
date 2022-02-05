from bs4 import BeautifulSoup
from .models import News
import gevent.monkey

import requests

session = requests.Session()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}
URL = 'https://remedium.ru/news/'


class Parser:
    def __init__(self, url, header):
        self.url = url
        self.header = header

    def getRequest(self):
        try:
            txt = session.get(url=self.url, headers=self.header, timeout=1)
            txt.encoding = 'utf8'
            return txt.text
        except Exception as ex:
            print(ex)
            return False

    def get_soup(self):
        if self.getRequest():
            html = self.getRequest()
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            return "<p>Ошибка отрисовки новостного контента</p>"


class DataNewsCreator:
    parser = Parser(URL, headers)
    soup = parser.get_soup()

    def create_news_data(self):
        try:
            news = self.soup.findAll('h3', {'class': 'b-section-item__title'})
            links = [item.find_next() for item in news]
            return [{'title': item['title'], 'link': f"https://remedium.ru{item['href']}"} for item in links]
        except Exception as ex:
            print(ex)
            return []
