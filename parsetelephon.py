import requests
from bs4 import BeautifulSoup
import sqlite3
import json

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Помилка:", response.status_code)
        return None

def parse_page_and_save(url, db_name, json_file):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rozetkapc (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            price REAL,
                            availability TEXT
                                            );
                                                ''')
        products_data = []
        products = soup.find_all('div', class_='goods-tile')
        for product in products:
            name = product.find('span', class_='goods-tile__title').text.strip()
            price_element = product.find('span', class_='goods-tile__price-value')
            price_str = price_element.text.strip()
            avafr = product.find('div', class_='goods-tile__availability')
            availability = avafr.text.strip()
            cursor.execute('''INSERT INTO rozetkapc (name, price, availability) VALUES (?, ?, ?)''',
                           (name, price_str, availability))
            product_data = {
                'name': name,
                'price': price_str,
                'availability': availability
            }
            products_data.append(product_data)
        conn.commit()
        conn.close()
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, ensure_ascii=False, indent=4)

        print("Дані було збережено", db_name, json_file)
url = 'https://rozetka.com.ua/djoysticks/c80173/'
db_name = 'rozetka.db'
json_file = 'rozetka.json'
parse_page_and_save(url, db_name, json_file)