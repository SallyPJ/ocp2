
import requests
from bs4 import BeautifulSoup
from scrapers import book_info_scraper
#import urllib3
import urllib.parse
import csv
from datetime import datetime
import os





website_url = "https://books.toscrape.com/index.html"
category_url_list = []
next_base_url = "https://books.toscrape.com/catalogue/category/books/fiction_10/"
cat_base_url = "https://books.toscrape.com/"
book_base_url = "https://books.toscrape.com/catalogue/"
response = requests.get(website_url)
soup = BeautifulSoup(response.text, "html.parser")


url_dico = {}

def retrieve_category_url(website_url):
    nav_list = soup.find("ul", class_="nav nav-list")
    li_tags = nav_list.find_all("li")
    result ={"category_name": [],"category_url": []}
    for li in li_tags:
        cat_href_index = li.find("a").get("href")
        cat_href = cat_href_index.replace("index.html", "")
        name = li.find("a").text.strip()
        result["category_name"].append(name)
        #url_dico["href"].append(cat_href)
        cat_full_url = urllib.parse.urljoin(cat_base_url, cat_href)
        result["category_url"].append(cat_full_url)

    del result["category_name"][0]
    del result["category_url"][0]

    #for name, full_url in zip(result["category_name"], result["category_url"]):
        #url_dico["name"] = full_url
    #url_dico = dict(zip(result["category_name"], result["category_url"]))
    for category_name, category_url in zip(result["category_name"], result["category_url"]):
        # Créer une entrée dans le dictionnaire avec le nom de catégorie comme clé
        # et un dictionnaire contenant une sous-clé "data" avec l'URL comme valeur
        url_dico[category_name] = {"category_main_url": category_url}
    print(url_dico)
    return url_dico


def search_for_next(url_dico):
    print(url_dico.keys())

    #urls = list(url_dico.items())
    #print(urls)
    for category, data in url_dico.items():
        url = data["category_main_url"]
        print(url)
        response3 = requests.get(url)
        soup = BeautifulSoup(response3.text, "html.parser")
        print(category)
        url_par_cat = []
        pages_to_scrap = {}
        url_par_cat.append(url)
        print(url)
        next_button = soup.find("li", class_="next")
        while next_button:
            next_partial_url = next_button.find("a").get("href")
            next_full_url = urllib.parse.urljoin(url, next_partial_url)
            url_par_cat.append(next_full_url)
            #print(next_partial_url)
            #print(next_full_url)
            response1 = requests.get(next_full_url)
            soup1 = BeautifulSoup(response1.text, "html.parser")
            next_button = soup1.find("li", class_="next")
        if not next_button:
            print("Il n'y a plus de bouton 'next'.")
        print(url_par_cat)
        pages_to_scrap = url_par_cat
        # Ajoute le sous-dictionnaire à la clé "Psychologie" de url_dico
        url_dico.setdefault(category,{})["pages_to_scrap"] = pages_to_scrap
        #ages_to_scrap["pages"] = url_par_cat
        # Ajoute le sous-dictionnaire à la clé "Psychologie" de url_dico

    print(url_dico)
    print(url_dico["Historical Fiction"])
    return url_dico





def retrieve_book_urls(url_dico):
    for category,category_data in url_dico.items():
        urls = category_data["pages_to_scrap"]
        books_link_list = []
        for url in urls:
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
        category_data["books_url"] = books_link_list
        print(category_data["books_url"])
    print(books_link_list)


#Récupère les urls des livres sur une page
def scrap_cat(url_dico):
    # Chemin absolu vers le répertoire du projet
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Chemin absolu vers le dossier "webscrapping" dans le répertoire du projet
    webscraping_directory = os.path.join(project_directory, "webscraping")

    # Créer un nom de dossier avec la date et l'heure du jour dans le répertoire du projet
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    folder_name = os.path.join(webscraping_directory, timestamp + "_webscraper_books-toscrape")

    # Créer le dossier s'il n'existe pas déjà
    os.makedirs(folder_name, exist_ok=True)

    print("Dossier créé le:", timestamp)


    for category,category_data in url_dico.items():
        list_of_books_url = category_data["books_url"]
        all_data = []
        for book in list_of_books_url:
            data = book_info_scraper.get_book_info(book)
            book_info_scraper.extract_book_image(data)
            all_data.append(data)
        csv_filename = os.path.join(folder_name, f"{category}.csv")
        write_to_csv1(all_data, csv_filename)



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

url_dico = retrieve_category_url(website_url)

search_for_next(url_dico)

retrieve_book_urls(url_dico)
scrap_cat(url_dico)
#retrieve_book_url(cat_url)
#search_for_next()
#scrap_cat(books_link_list)