import requests
from bs4 import BeautifulSoup
import pandas as pd

product_page_url = "http://books.toscrape.com/catalogue/unicorn-tracks_951/index.html"

response = requests.get(product_page_url)
# print(response.encoding) : The encoding isn't in UTF-8 : wrong format
response.encoding = 'utf-8'

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('title').text

    tds = soup.findAll('td')
    listeTD =[]
    for td in tds:
        listeTD.append(str(td.string))
    universal_product_code = listeTD[0]
    price_including_tax = listeTD[2]
    price_excluding_tax = listeTD[3]
    number_available = listeTD[5]
    review_rating = listeTD[6]

    product_description = soup.find(id = 'product_description').find_next('p').string

    category = soup.find(class_ = 'breadcrumb').find(text = 'Books').findNext('a').string

    image_url = 'http://books.toscrape.com/' + soup.find(class_ = 'carousel-inner').find('img')['src'].\
        replace('../../', '')

df = pd.DataFrame({'product_page_url' : [product_page_url],
                   'universal_ product_code' : [universal_product_code],
                   'title' : [title],
                   'price_including_tax' : [price_including_tax],
                   'price_excluding_tax' : [price_excluding_tax],
                   'number_available' : [number_available],
                   'product_description' : [product_description],
                   'category' : [category],
                   'review_rating' : [review_rating],
                   'image_url' : [image_url]})

df.to_csv('extraction des prix.csv')
