import requests
from bs4 import BeautifulSoup

url = 'https://www.zomato.com/melbourne/restaurants/cafes'

def get_html_file():
    # User-Agent buat ngehindarin error 403
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # buat file html, biar ngga berulang kali request
    f = open('./res.html', 'w+')
    f.write(req.text)
    f.close()

# get_html_file()

soup = BeautifulSoup(open('./res.html'), 'html.parser')

cuisine = soup.find('h1', class_='search_title').string

card = soup.find('div', class_='card search-snippet-card search-card')

# pertama dapetin areanya dulu, terus dapetin semua text di tag span
asso_cuisine = card.find('span', class_='col-s-11 col-m-12 nowrap pl0').text
organisation = card.find('a', class_='result-title').text
address = card.find('')
location = card.find('a', class_='search_result_subzone').text
phone = card.find('a', class_='res-snippet-ph-info')['data-phone-no-str']

print(phone)