from book_info import get_book_info, write_to_csv
import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv



cat_url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
next_base_url = "https://books.toscrape.com/catalogue/category/books/fiction_10/"
book_base_url = "https://books.toscrape.com/catalogue/"
response = requests.get(cat_url)
soup = BeautifulSoup(response.text, "html.parser")
books_link_list =[]
all_data = []
url_list = []
#Récupère les urls des livres sur une page


#Récupère la liste des urls des livres de chaque page d'une catégorie
def retrieve_book_urls(url_list):
    for url in url_list:
        response2 = requests.get(url)
        soup2 = BeautifulSoup(response2.text, "html.parser")
        product_articles = soup2.find_all("article", class_="product_pod")
        for article in product_articles:
            h3_tag = article.find("h3")
            link = h3_tag.find("a").get("href")
            parts = link.split('/')
            book_partial_url = parts[-2] + '/' + parts[-1]
            print(book_partial_url)
            book_full_url = urllib.parse.urljoin(book_base_url, book_partial_url)
            books_link_list.append(book_full_url)
    print(books_link_list)
    return books_link_list
#Récupère l'url d'une page Next (en cours)

def search_for_next(url_cat):

    url_list.append(cat_url)
    next_button = soup.find("li", class_="next")
    while next_button:
        next_partial_url = next_button.find("a").get("href")
        next_full_url = urllib.parse.urljoin(next_base_url, next_partial_url)
        url_list.append(next_full_url)
        print(next_partial_url)
        print(next_full_url)
        response1 = requests.get(next_full_url)
        soup1 = BeautifulSoup(response1.text, "html.parser")
        next_button = soup1.find("li", class_="next")
    if not next_button:
        print("Il n'y a plus de bouton 'next'.")
    print(url_list)
    return url_list

#Récupère les urls des livres sur une page
def scrap_cat(books_link_list):
    for url in books_link_list:
        data = get_book_info(url)
        all_data.append(data)
    write_to_csv1(all_data, "../cat.csv")

#Ecrit les données des livres sur un csv
def write_to_csv1(data_list, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category",
                      "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)




search_for_next(cat_url)
retrieve_book_urls(url_list)
scrap_cat(books_link_list)