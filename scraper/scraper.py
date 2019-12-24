import requests
from bs4 import BeautifulSoup
import csv

soup = BeautifulSoup(requests.get('https://oz.by/books/topic16.html?availability=1').text, 'html.parser')
last_page = soup.findAll(class_ = "g-pagination__list__item")[-1].getText()
last_page = int(last_page)

with open('data.csv', 'w') as csv_file:
	csv_writer = csv.writer(csv_file)
	headers = ['Title', 'Price', 'Link']
	csv_writer.writerow(headers)

	base_url = 'https://oz.by/books/topic16.html?availability=1&page='
	for page_number in range(1,last_page+1):
		url = base_url + str(page_number)
		soup = BeautifulSoup(requests.get(url).text, 'html.parser')
		goods_unscr = soup.findAll(class_ =  "item-type-card__inner")
		for product in goods_unscr:
		 	title = product.find(class_="item-type-card__title").getText()
		 	price = product.find(class_="item-type-card__btn").getText().strip()
		 	link = 'https://oz.by/books' + product.find(class_="item-type-card__link").get('href')
		 	csv_writer.writerow([title, price, link])