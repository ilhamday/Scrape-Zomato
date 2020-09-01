import requests, csv, time
from bs4 import BeautifulSoup

# udah diganti pake fungsi checking_category
# url = 'https://www.zomato.com/melbourne/restaurants/chinese'

# def get_detail(total_page):
def get_detail():

    # buat dapetin total_page tanpa ekseskusi no 2, kalau html file udah tersedia di result.html
    soup = BeautifulSoup(open(f'./result_html/res1.html'), 'html.parser')
    total_page = soup.find('div', class_='pagination-number').find('div').find('b').find_next_sibling('b').text

    total_page = int(total_page)

    for page in range(total_page):

        page += 1
        # ini isi soupny audah beda lagi sama yang ada diatas for.
        soup = BeautifulSoup(open(f'./result_html/res{page}.html'), 'html.parser')

        cards = soup.find_all('div', class_='card search-snippet-card search-card')
        cuisine = soup.find('h1', class_='search_title').text
        print('Adding data to csv...')

        for card in cards:

            asso_cuisine = card.find('span', class_='col-s-11 col-m-12 nowrap pl0').text
            organisation = card.find('a', class_='result-title').text
            address = card.find('div', class_='search-result-address').text
            location = card.find('a', class_='search_result_subzone').text
            phone = card.find('a', class_='res-snippet-ph-info')['data-phone-no-str']

            # masukin character, contoh -> ', Caroline' Springs ke variable cut | dipakai buat split terus diambil item pertama yaitu addressnya
            cut = f', {location}'
            x = address.strip().split(cut)

            # strip() digunain untuk ngilangin spasi
            cuisine = cuisine.strip()
            organisation = organisation.strip()

            writer = csv.writer(open('./test.csv', 'a', newline='', encoding='utf-8'))  # method a -> append
            data = [cuisine, asso_cuisine, organisation, x[0], location, phone]
            writer.writerow(data)

# PAGINATION
def get_urls_create_html(url_checked):
    print('Getting urls...')

    print(url_checked)

    req = requests.get(url_checked, headers={'User-Agent': 'Mozilla/5.0'}) # 1 kali req
    soup = BeautifulSoup(req.text, 'html.parser')

    # dapetin total page, mulai dari div dengan class -> ke anaknya -> anakknya lagi -> sodara anaknya
    total_page = soup.find('div', class_='pagination-number').find('div').find('b').find_next_sibling('b').text
    total_page = int(total_page)

    # list_urls = []

    # for page in range(2):
    for page in range(total_page):
        page += 1
        print(f'Creating res{page}.html ...')
        # request urlnya | query string parameter | methodnya
        # url -> https://www.zomato.com/melbourne/restaurants/cafes?page=5
        # request url -> https://www.zomato.com/melbourne/restaurants/cafes    <- masih di bagian cafes, belum di kategori laen
        # query -> page= nomor halaman
        # method -> get
        params = {
            'page': page
        }

        # User-Agent buat ngehindarin error 403
        req = requests.get(url_checked, params=params, headers={'User-Agent': 'Mozilla/5.0'}) # request berdasarkan pagenya

        # print(req.url) <- buat print urlnya uncomment aja kalau mau coba

        # list_urls.append(req.url)

        # buat file html, biar ngga berulang kali request
        f = open(f'./result_html/res{page}.html', 'w+')
        f.write(req.text)
        f.close()

        if page % 5 == 0:
            print('Wait for 5 sec')
            time.sleep(5)

        # uncomment if you just want to try it, after 2 html it will break
        # if page == 2:
        #     break

    return total_page

def create_csv():
    # Buat file csv
    writer = csv.writer(open('./test.csv', 'w', newline=''))  # method w -> write
    headers = ['Cuisine', 'Assosiation Cuisine', 'Organisation', 'Address', 'Location', 'Phone']
    writer.writerow(headers)

def checking_categroy_url(url_with_categoty):
    print(f'Checking url...')

    check_url = requests.get(url_with_categoty, headers={'User-Agent': 'Mozilla/5.0'})

    if check_url.status_code == 200:
        print('Category found!')
        url_checked = url_with_categoty
        return url_checked
    else:
        print('Category not found!!!')

def run():
    while True:
        options = int(input('\n--------'
                            '\n1.Check Category '
                            '\n2.Get HTML files '
                            '\n3.Create csv file'
                            '\n4.Get details'
                            '\n5.Exit'
                            '\nInput number: '))

        if options == 1:
            url = 'https://www.zomato.com/melbourne/restaurants/'
            categoty = input('Input Category: ')

            url_with_category = url + categoty

            url_checked = checking_categroy_url(url_with_category)

        if options == 2:
            # total_page = get_urls(url_checked)
            get_urls_create_html(url_checked)

        if options == 3:
            print('Creating csv...')
            create_csv()

        if options == 4:
            print('Getting details...')
            # kalau pakai ini, options 1 nya harus dijalanin dulu, karena kalau nggak total_page nya -> None
            # get_detail(total_page)
            get_detail()

        if options == 5:
            exit()

if __name__ == '__main__':
    run()
