import requests
from bs4 import BeautifulSoup

url = 'https://www.zomato.com/melbourne/restaurants/cafes'

req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(req.text, 'html.parser')

print(soup.find('h1').string)