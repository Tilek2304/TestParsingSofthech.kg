import requests
import csv
import json
from bs4 import BeautifulSoup
from bs4 import Tag, ResultSet
from settings import URL

headers = {
    'User-Agent': 'xiaomi_probook_15.6',
    'From': 'esenaliev2304@gmail.com'  # This is another valid field
}
response = requests.get(URL, headers=headers)

def get_html_card():        # Данная функция возвращает все html карты товаров
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'lxml')
    cards: ResultSet = soup.find_all('div', class_="product-thumb transition")
    return cards

def parse_cards(cards):
    obj_list = []
    for i in cards:
        obj = {
            'link': i.find('div', class_='name').find('a').get('href'),
            'price': str(i.find('div', class_='price').text),
            'title':i.find('div', class_='name').a.text,
            'small-description':i.find('div',class_='description-small').text
        }
        obj_list.append(obj)
    with open('jsonDB.json', 'w') as f:
        json.dump(obj_list, f, indent=4, ensure_ascii=True)
    with open('csvDB.csv', 'w') as file:
        fieldnames = obj_list[0].keys()
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(obj_list)

cards = get_html_card()
parse_cards(cards)