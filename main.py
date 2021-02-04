import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil

''' 
Function of scrapping one book with the url of the book.
It saves the picture of the book in the file of the category.
It returns a Dataframe with the values product_page_url, universal_product_code, title, price_including_tax, 
price_excluding_tax , number_available, product_description, category, review_rating, image_url.
'''


def book_scrapping(url_book):
    response_url_book = requests.get(url_book)
    response_url_book.encoding = 'utf-8'

    if response_url_book.ok:
        soup_book = BeautifulSoup(response_url_book.text, 'lxml')
        product_page_url = url_book
        title = soup_book.find('title').text.split('|')[0].strip()  # delete spaces before and after the text

        tds = soup_book.findAll('td')
        list_td = []
        for td in tds:
            list_td.append(str(td.string))
        universal_product_code = list_td[0]
        price_including_tax = list_td[2]
        price_excluding_tax = list_td[3]
        number_available = list_td[5]

        review_rating = soup_book.find(class_="product_page").find(class_="star-rating").attrs['class'][1]
        if review_rating == 'One':
            review_rating = review_rating + ' star'
        else:
            review_rating = review_rating + ' stars'

        if soup_book.find(id='product_description') is not None:  # Some books haven't description
            product_description = soup_book.find(id='product_description').find_next('p').string
        else:
            product_description = ''

        category_book = soup_book.find(class_='breadcrumb').find(text='Books').findNext('a').string

        image_url = 'http://books.toscrape.com/' + soup_book.find(class_='carousel-inner').find('img')['src']. \
            replace('../../', '')

        response_image = requests.get(image_url)
        file = open(title.replace('/', '').replace(':', '').replace('"', '') + '.jpg', 'wb')  # w:write, b:binary
        file.write(response_image.content)
        file.close()

        return {'product_page_url': product_page_url,
                'universal_ product_code': universal_product_code,
                'title': title,
                'price_including_tax': price_including_tax,
                'price_excluding_tax': price_excluding_tax,
                'number_available': number_available,
                'product_description': product_description,
                'category': category_book,
                'review_rating': review_rating,
                'image_url': image_url}


''' 
Function of scrapping one category of books with the url of the category. 
The function scans all the books in the category.
It writes a file .csv with the data of each book. 
'''


def category_scrapping(url_category):
    df = pd.DataFrame(columns={'product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                               'price_excluding_tax', 'number_available', 'product_description', 'category',
                               'review_rating', 'image_url'})  # Dataframe initializing
    next_page = 0  # Initializing of next_page for the first pass
    url_root_category = url_category
    while next_page is not None:  # While there is a next page
        response_category = requests.get(url_category)
        response_category.encoding = 'utf-8'
        if response_category.ok:
            soup_category = BeautifulSoup(response_category.text, 'lxml')
            h3s = soup_category.findAll('h3')
            category = soup_category.find(class_='page-header action').find('h1').string
            if next_page == 0:
                os.mkdir(category)
                os.chdir(category)
            for h3 in h3s:  # Loop on all the books of the page
                url_book = 'http://books.toscrape.com/catalogue/' + h3.find('a')['href'].replace('../../../', '')
                df = df.append(book_scrapping(url_book), ignore_index=True)
                next_page = soup_category.find(class_='next')
            if next_page is not None:  # If None, the next instruction returns a error
                url_category = url_root_category + '/' + str(next_page.find('a')['href'])
            else:
                df.to_csv(category + '.csv', index=False)
                print(category + ' scraped')  # Information for terminal
    os.chdir("..")  # Set the current directory to the parent directory use


''' 
Function of scrapping of the all website http://books.toscrape.com/index.html
The function prepares the repertory of results and called the 2 other functions for scrapping all the website and 
writing the .csv and the pictures by category.
'''


def main():
    if os.path.exists("Results"):  # If already executed
        shutil.rmtree("Results")  # delete the directory and its files
        os.mkdir("Results")  # Creating a directory for data and pictures
    else:
        os.mkdir("Results")
    os.chdir("Results")
    url = 'http://books.toscrape.com/index.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    links = []
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        a_list = soup.find(class_='side_categories').findAll('a')
        for a in a_list:
            if a['href'] != 'catalogue/category/books_1/index.html':
                links.append('http://books.toscrape.com/' + str(a['href']).replace('index.html', ''))

    for link in links:
        category_scrapping(link)


main()
