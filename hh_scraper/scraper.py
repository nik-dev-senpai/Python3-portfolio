#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import regex
import math
import numpy as np
import csv

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 6.0; Win64; x64; Trident/5.0; .NET CLR 3.8.50799; Media Center PC 6.0; .NET4.0E)"}
request_link = 'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python'
try:
  response = requests.get(request_link, headers = headers).text
except:
  print("An exception occurred")
  exit()

html = BeautifulSoup(response, 'html.parser')

#pagination

#getting total vacancies amount
items_amount_string = html.findAll(class_ = "bloko-header-1")[-1].getText()
items_amount_array = regex.findall(r'\d+', items_amount_string, flags=regex.ASCII)
items_amount = ""
for elem in items_amount_array:
	items_amount += elem
items_amount = int(items_amount)
#getting vacancies amount on single page
items_on_page = len(html.findAll(class_ = "resume-search-item__name"))
#hh.ru allows to see only 2000 vacancies without filtration. 
#So either we can scrape 2000 vacancies or less
if items_amount > 2000:
	items_amount = 2000
#then we calculating amount of pages we need to scrape and round it
pages_amount = items_amount/items_on_page
pages_amount = math.ceil(pages_amount)

#getting array of all pages
default_link = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=python&page='
links_array = []
for page_number in range(0, pages_amount):
	page_link = default_link + str(page_number)
	links_array.append(page_link)

#getting array of all vacancies links
vacancies_hrefs = []
for page_link in links_array:
	try:
	  response = requests.get(page_link, headers = headers).text
	except:
	  print("An exception occurred")
	  exit()
	html = BeautifulSoup(response, 'html.parser')
	vacancies_unscraped = html.find_all(class_ = "HH-LinkModifier")
	for link_html in vacancies_unscraped:
		href = link_html.get('href')
		vacancies_hrefs.append(href)

#getting all key skills and sorting them
key_skills_all = []
i = 1
for href in vacancies_hrefs:
	response = requests.get(href, headers = headers).text
	html = BeautifulSoup(response, 'html.parser')
	skills_unparsed = html.findAll(class_ = "bloko-tag__section_text")
	print('scrapping ' + str(i))
	i = int(i) + 1
	for item in skills_unparsed:
		item = item.getText()
		key_skills_all.append(item)
key_skills_all.sort()
key_skills_all = np.array(key_skills_all)
(unique, counts) = np.unique(key_skills_all, return_counts=True)
key_skills = np.asarray((unique, counts)).T

#and finally recording it to csv
file_name = request_link.split('text=')[1] + '.csv'
with open(file_name, 'w') as csv_file:
	csv_writer = csv.writer(csv_file)
	headers = ['skill', 'frequency']
	csv_writer.writerow(headers)
	for row in key_skills:
		csv_writer.writerow(row)
