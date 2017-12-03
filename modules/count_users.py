import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


def count_users():
    """
    Определение общего количества пользователей.

    :return: количество пользователей
    """

    catalog_page = 'https://vk.com/catalog.php'

    while True:
        catalog = requests.get(catalog_page)
        soup = BeautifulSoup(catalog.text, 'html.parser')

        catalog_wrap = soup.find('div', class_='catalog_wrap clear_fix')
        tags = catalog_wrap.find_all(href=re.compile('catalog\.php\?selection=.*'))

        if not tags:
            return int(catalog_wrap.find_all(href=re.compile('id\d+'))[-1].get('href')[2:])

        catalog_page = urljoin(catalog_page, tags[-1].get('href'))
