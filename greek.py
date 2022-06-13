# python - exploring customer reviews of greek restaurants in Frankfurt
# listed on tripadvisor.de

import webbrowser
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
html_text = requests.get(
    'https://www.tripadvisor.de/Restaurants-g187337-c23-Frankfurt_Hesse.html', headers=headers).text.encode('utf-8').decode('ascii', errors='ignore')

# we instantiate a BeautifulSoup objec to read the html content

soup = BeautifulSoup(html_text, 'lxml')
restaurants = soup.find_all(
    'div', class_='emrzT Vt o')
review_counts = soup.find_all('span', class_='NoCoR')


# figuring out the URL of each restaurant needed  to grab the split by rating category

href_list = []
prefix = str('https://www.tripadvisor.de')

for restaurant in restaurants:
    href = restaurant.find('a').get('href')
    href_list.append(prefix + href)
url = href_list[0]


# entering each URL and scraping the rating split by category


url_text = requests.get(url, headers=headers).text.encode(
    'utf-8').decode('ascii', errors='ignore')


url_soup = BeautifulSoup(url_text, 'lxml')
dict = dict({'name': [], 'five_star': [], 'four_star': [],
            'three_star': [], 'two_star': [], 'one_star': []})


for r in range(len(href_list)):
    url = href_list[r]
    url_text = requests.get(url, headers=headers).text.encode(
        'utf-8').decode('ascii', errors='ignore')
    url_soup = BeautifulSoup(url_text, 'lxml')
    resto = url_soup.find('h1', class_='fHibz')
    dict['name'].append(resto.text)
    choices = url_soup.find_all('span', class_='row_num')[:5]
    dict['five_star'].append(choices[0].text)
    dict['four_star'].append(choices[1].text)
    dict['three_star'].append(choices[2].text)
    dict['two_star'].append(choices[3].text)
    dict['one_star'].append(choices[4].text)

# saving the data into an excel sheet
df = pd.DataFrame(dict)
df.to_excel(
    r'C:\Users\steff\Desktop\webpage_project\greek\greek_restaurants.xlsx', index=False)
