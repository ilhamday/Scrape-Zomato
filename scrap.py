soup = BeautifulSoup(open('./res.html'), 'html.parser')

cuisine = soup.find('h1', class_='search_title').string

cards = soup.find_all('div', class_='card search-snippet-card search-card')

for card in cards:
    asso_cuisine = card.find('span', class_='col-s-11 col-m-12 nowrap pl0').text
    organisation = card.find('a', class_='result-title').text
    address = card.find('div', class_='search-result-address').text
    location = card.find('a', class_='search_result_subzone').text
    phone = card.find('a', class_='res-snippet-ph-info')['data-phone-no-str']

    # masukin character, contoh -> , Caroline Springs ke variable cut | dipakai buat split terus diambil item pertama yaitu addressnya
    cut = f', {location}'
    x = address.strip().split(cut)

    #strip()    digunain    untuk    ngilangin    spasi
    print(f'cuisine = {cuisine.strip()}')
    print(f'assosiation cuisine = {asso_cuisine}')
    print(f'organisation = {organisation.strip()}')
    print(f'address = {x[0]}')
    print(f'location = {location}')
    print(f'phone = {phone}')
    print('---------')
