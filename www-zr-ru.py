import json
import requests
from bs4 import BeautifulSoup

URL = 'https://www.zr.ru/news/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0', 'accept': '*/*'}
HOST = 'https://www.zr.ru'


def get_html(url, params=None):                                 # Определяю функцию  # params - для определения числа страниц
    r = requests.get(url, headers=HEADERS, params=params)       # С помощью requests делается get-запрос к серверу 
    return r                                                    # Обьект r будет возвращён и использован в функции parse()


def get_content(html):                                          # Функция сбора данных с сайта
    soup = BeautifulSoup(html, 'html.parser')                   # Для получения обьекта soup - обращаемся к конструктору BeautifulSoup, указываем тип документа 'html.parser'
    items = soup.find_all('article', class_='story-short')

    news = []
    for item in items[:10]:                                     # 11й элемент отсутсвует на первой странице. Чтобы собрать больше статей требуется пагинация
        details = get_article_content(HOST + item.find('a', class_='link').get('href'))

        news.append({
            'title': item.find('a', class_='link').get_text(strip=True),
            'link': HOST + item.find('a', class_='link').get('href'),
            'article': item.find('div', class_='articles__item-desc').get_text(strip=True),
            'picture': HOST + item.find('img').get('src'),
            'autor': details['autor'],
            'date': details['date']
        })
    print(news)
    with open("db_zr.json", "w") as jfile:
        json.dump(news, jfile, indent=4, ensure_ascii=False)


def get_article_content(article_url):
    html = get_html(article_url)
    soup = BeautifulSoup(html.text, 'html.parser') 
    items = soup.find('body', class_='zr')
    return {
        'autor': items.find('span', class_='link_pink').get_text(strip=True),
        'date': items.find('div', class_='info__date').get_text(strip=True)
        }


def parse():                                    # Основная функция
    html = get_html(URL)                        # Парсим первую страницу
    if html.status_code == 200:                 # Проверяем status_code (связь со страицей)
        get_content(html.text)
    else:
        print('Error')   

parse()                                         # Вызов функции parse
