"""
Extraire les données d'un seul produit :
Choisissez n'importe quelle page Produit sur le site de Books to Scrape. Écrivez un
script Python qui visite cette page et en extrait les informations suivantes :
● product_page_url
● universal_ product_code (upc)
● title
● price_including_tax
● price_excluding_tax
● number_available
● product_description
● category
● review_rating
● image_url
Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme
en-têtes de colonnes.
Questions :
- Déterminer les fonctions
- Fonction lambda : need explication
- Taxes : souci du site ou c'est à nous de faire le calcul ?
- Catégorie : Books? History ?
"""

import requests
from bs4 import BeautifulSoup
import csv


#J methode avec le paramètre du livre get_book_info, faire la même chose par categorie,


def get_book_info(url):
    # Récupérer le contenu de la page
    response = requests.get(url)

    # Vérifier que le lien est toujours actif
    if response.ok:
        response.text
    else:
        print("La requête a échoué.")

    # Parser le HTLM avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire l'URL de la page
    product_page_url = response.url


    # Extraire le titre de la page
    product_main_div = soup.find("div", class_="col-sm-6 product_main")
    h1_tag = product_main_div.find("h1")
    title = h1_tag.get_text()

    # Extraire la note
    product_main_div = soup.find('div', class_='col-sm-6 product_main')
    # Trouver toutes les balises <p> avec une classe qui commence par "star-rating"
    star_rating_class = product_main_div.find('p', class_= lambda x: x and x.startswith('star-rating'))
    class_name = star_rating_class.get('class')
    review_rating = class_name[1]



    # Trouver la table de classe spécifique
    table = soup.find('table', class_="table table-striped")
    td_tags = table.find_all('td')

    # Initialiser les variables pour stocker les valeurs extraites
    universal_product_code = ""
    category = ""
    price_excluding_tax = ""
    price_including_tax = ""
    number_available = ""

    # Parcourir les balises séléctionnée <td> et associer leur contenu à une variable
    for i, td in enumerate(td_tags):
        if i == 0:
            universal_product_code = td.text.strip()
        elif i == 1:
            category = td.text.strip()
        elif i == 2:
            price_excluding_tax = td.text.strip()
        elif i == 3:
            price_including_tax = td.text.strip()
        elif i == 5:
            number_available = td.text.strip()


    # Extraire l'url de l'image
    parent_div = soup.find("div", class_="item active")
    # Trouver la balise <img> à l'intérieur de la balise parent
    img_tag = parent_div.find("img")
    # Extraire l'URL de l'image
    relative_path = img_tag.get("src")
    base_url = "https://books.toscrape.com/"
    image_url = base_url + relative_path

    # Extraire la description du produit
    # Trouver la balise <meta> avec l'attribut name="description"
    description = soup.find("meta", attrs={"name": "description"})
    # Extraire le contenu de l'attribut "content"
    product_description = description.get("content") if description else None

    page_dictionnary = {
        "product_page_url": product_page_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }
    print(page_dictionnary)
    return page_dictionnary


def write_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category",
                      "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)


if __name__ == '__main__':
    url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
    book_info = get_book_info(url)
    if book_info:
        write_to_csv(book_info, "product_info.csv")
    else:
        print("Les informations du livre n'ont pas pu être récupérées.")
