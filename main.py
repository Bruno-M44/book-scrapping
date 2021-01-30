import requests
from bs4 import BeautifulSoup
import pandas as pd


def book_scrapping(url_book):
    response_url_book = requests.get(url_book)
    response_url_book.encoding = 'utf-8'

    if response_url_book.ok:
        soup_book = BeautifulSoup(response_url_book.text, 'lxml')
        product_page_url = url_book
        title = soup_book.find('title').text

        tds = soup_book.findAll('td')
        list_td = []
        for td in tds:
            list_td.append(str(td.string))
        universal_product_code = list_td[0]
        price_including_tax = list_td[2]
        price_excluding_tax = list_td[3]
        number_available = list_td[5]
        review_rating = list_td[6]

        if soup_book.find(id='product_description') is not None:  # Some books haven't description
            product_description = soup_book.find(id='product_description').find_next('p').string
        else:
            product_description = ''

        category = soup_book.find(class_='breadcrumb').find(text='Books').findNext('a').string

        image_url = 'http://books.toscrape.com/' + soup_book.find(class_='carousel-inner').find('img')['src']. \
            replace('../../', '')

        response_image = requests.get(image_url)
        file = open(image_url.split('/')[-1], "wb")
        file.write(response_image.content)
        file.close()

        return {'product_page_url': product_page_url,
                'universal_ product_code': universal_product_code,
                'title': title,
                'price_including_tax': price_including_tax,
                'price_excluding_tax': price_excluding_tax,
                'number_available': number_available,
                'product_description': product_description,
                'category': category,
                'review_rating': review_rating,
                'image_url': image_url}


def category_scrapping(url_category):
    df = pd.DataFrame(columns={'product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                               'price_excluding_tax', 'number_available', 'product_description', 'category',
                               'review_rating', 'image_url'})  # Dataframe initializing
    response_category = requests.get(url_category)
    response_category.encoding = 'utf-8'

    if response_category.ok:
        soup_category = BeautifulSoup(response_category.text, 'lxml')
        h3s = soup_category.findAll('h3')
        category = soup_category.find(class_='page-header action').find('h1').string
        for h3 in h3s:  # Loop on all the books of the page
            url_book = 'http://books.toscrape.com/catalogue/' + h3.find('a')['href'].replace('../../../', '')
            df = df.append(book_scrapping(url_book))  # ignore_index=True : utile ?
        next_page = soup_category.find(class_='next')
        while next_page is not None:  # While there is a next page
            url_book = url_category + '/' + str(
                next_page.find('a')['href'])
            response_book = requests.get(url_book)
            response_book.encoding = 'utf-8'
            if response.ok:
                soup = BeautifulSoup(response.text, 'lxml')
                h3s = soup.findAll('h3')
                for h3 in h3s:
                    a = h3.find('a')
                    product_page_url = 'http://books.toscrape.com/catalogue/' + a['href'].replace('../../../', '')
                    df = df.append(book_scrapping(product_page_url), ignore_index=True)
                next_page = soup.find(class_='next')
    df.to_csv(category + '.csv')
    print(category + ' scraped')  # Information for terminal


url = 'http://books.toscrape.com/index.html'
response = requests.get(url)
response.encoding = 'utf-8'

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    aList = soup.find(class_='side_categories').findAll('a')
    links = []
    for a in aList:
        if a['href'] != 'catalogue/category/books_1/index.html':
            links.append('http://books.toscrape.com/' + str(a['href']).replace('index.html', ''))

df1 = pd.DataFrame(columns=['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                            'price_excluding_tax', 'number_available', 'product_description', 'category',
                            'review_rating', 'image_url'])
for link in links:
    category_scrapping(link)
