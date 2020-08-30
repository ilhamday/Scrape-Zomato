import re
import requests, csv, time
from bs4 import BeautifulSoup

url = 'https://www.zomato.com/melbourne/restaurants/cafes'


def get_html_file(url_requested, page):
    print('Getting pages...')
    # User-Agent buat ngehindarin error 403
    req = requests.get(url_requested, headers={'User-Agent': 'Mozilla/5.0'})

    # buat file html, biar ngga berulang kali request
    f = open(f'./result_html/res{page}.html', 'w+')
    f.write(req.text)
    f.close()


def get_detail(page):
    print('Getting details...')
    soup = BeautifulSoup(open(f'./res{page}.html'), 'html.parser')

    cuisine = soup.find('h1', class_='search_title').text

    cards = soup.find_all('div', class_='card search-snippet-card search-card')

    n = 0
    print('Adding to csv...')
    for card in cards:
        asso_cuisine = card.find('span', class_='col-s-11 col-m-12 nowrap pl0').text
        organisation = card.find('a', class_='result-title').text
        address = card.find('div', class_='search-result-address').text
        location = card.find('a', class_='search_result_subzone').text
        phone = card.find('a', class_='res-snippet-ph-info')['data-phone-no-str']

        # masukin character, contoh -> , Caroline Springs ke variable cut | dipakai buat split terus diambil item pertama yaitu addressnya
        cut = f', {location}'
        x = address.strip().split(cut)
        # strip() digunain untuk ngilangin spasi
        cuisine = cuisine.strip()
        organisation = organisation.strip()

        n = n + 1
        # print(f'{n}. cuisine = {cuisine}')
        # print(f'assosiation cuisine = {asso_cuisine}')
        # print(f'organisation = {organisation.strip()}')
        # print(f'address = {x[0]}')
        # print(f'location = {location}')
        # print(f'phone = {phone}')
        # print('---------')

        writer = csv.writer(open('./test.csv', 'a', newline='', encoding='utf-8'))  # method a -> append
        data = [cuisine, asso_cuisine, organisation, x[0], location, phone]
        writer.writerow(data)


# PAGINATION
def get_urls():
    print('Getting urls...')
    soup = BeautifulSoup(open('/res.html'), 'html.parser')
    # dapetin total page, mulai dari div dengan class -> ke anaknya -> anakknya lagi -> sodara anaknya
    total_page = soup.find('div', class_='pagination-number').find('div').find('b').find_next_sibling('b').text
    total_page = int(total_page)

    list_urls = []

    # for page in range(2):
    for page in range(total_page):
        page += 1

        # request urlnya | query string parameter | methodnya
        # url -> https://www.zomato.com/melbourne/restaurants/cafes?page=5
        # request url -> https://www.zomato.com/melbourne/restaurants/cafes    <- masih di bagian cafes, belum di kategori laen
        # query -> page= nomor halaman
        # method -> get
        params = {
            'page': page
        }

        # User-Agent buat ngehindarin error 403
        req = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})

        # print(req.url) <- buat print urlnya uncomment aja kalau mau coba
        url_requested = req.url
        # coba buat html
        get_html_file(url_requested, page)

        if page % 5 == 0:
            print('Wait for 5 sec')
            time.sleep(5)

        if page == 20:
            break

def create_csv():
    # Buat file csv
    print('Creating csv...')
    writer = csv.writer(open('./test.csv', 'w', newline=''))  # method w -> write
    # yang mau diambil dijadiin Header
    headers = ['Cuisine', 'Assosiation Cuisine', 'Organisation', 'Address', 'Location', 'Phone']
    writer.writerow(headers)

    soup = BeautifulSoup(open('./res.html'), 'html.parser')
    # dapetin total page, mulai dari div dengan class -> ke anaknya -> anakknya lagi -> sodara anaknya
    total_page = soup.find('div', class_='pagination-number').find('div').find('b').find_next_sibling('b').text
    total_page = int(total_page)

    for page in range(total_page):
        page += 1
        get_detail(page)


def run():
    options = int(input('1. Collecting URL\n2. Collecting HTML file\n3. Create CSV\n'))

    if options == 1:
        get_urls()

    if options == 2:
        get_html_file()

    if options == 3:
        create_csv()


if __name__ == '__main__':
    run()
