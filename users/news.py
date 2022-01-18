from bs4 import BeautifulSoup

import requests

session = requests.Session()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
URL = 'https://ria.ru/tag_medicina/'


class Parser:
    def __init__(self, url, header):
        self.url = url
        self.header = header
        self.html = session.get(url=self.url, headers=self.header).text

    def get_soup(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        return soup

    def create_html(self):
        pretty = self.get_soup().prettify()
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(pretty)


def news_content_circle_wrapper(func):
    def wrapper_around(elem):
        for item in elem:
            for el in item.children:
                if el != '\n':
                    func(el)


class DataNewsCreator:
    parser = Parser(URL, headers)
    soup = parser.get_soup()

    def create_news_data(self):
        try:
            news = self.soup.findAll('a', {'class': 'list-item__title'})
            return [{'title': item.text, 'link': item['href']} for item in news]
        except:
            print('Ошибка отрисовки новостного контента')
            return []
