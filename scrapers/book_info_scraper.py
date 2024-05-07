import requests
from bs4 import BeautifulSoup
import csv
import re
from word2number import w2n
import urllib.request
import os
from datetime import datetime




def get_book_info(url):
    # Récupérer le contenu de la page
    response = requests.get(url)

    # Vérifier que le lien est toujours actif
    if response.ok:
        response.text
    else:
        print("Le lien de la page est cassé.")

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
    review_rating_raw = class_name[1]
    review_rating = (w2n.word_to_num(review_rating_raw))

    # Extraire la catégorie
    cat = soup.find("ul", class_="breadcrumb")
    li_tags = cat.find_all("li")
    category = li_tags[2].text.strip()

    # Trouver la table de classe spécifique
    table = soup.find('table', class_="table table-striped")
    td_tags = table.find_all('td')

    # Initialiser les variables pour stocker les valeurs extraites
    universal_product_code = ""
    price_excluding_tax = ""
    price_including_tax = ""
    number_available = ""

    # Parcourir les balises séléctionnée <td> et associer leur contenu à une variable
    for i, td in enumerate(td_tags):
        if i == 0:
            universal_product_code = td.text.strip()
        elif i == 2:
            price_excluding_tax_text = td.text.strip()
            price_excluding_tax = price_excluding_tax_text.split("£")[1]
        elif i == 3:
            price_including_tax_text = td.text.strip()
            price_including_tax = price_including_tax_text.split("£")[1]
        elif i == 5:
            number_available_text = td.text.strip()
            number_available = int(re.findall(r"\d+", number_available_text )[0])
        else:
            pass

    # Extraire l'url partielle de l'image
    parent_div = soup.find("div", class_="item active")
    # Trouver la balise <img> à l'intérieur de la balise parent
    img_tag = parent_div.find("img")
    # Concaténer les 2 urls
    relative_path = img_tag.get("src")
    base_url = "https://books.toscrape.com/"
    image_url = urllib.parse.urljoin(base_url, relative_path)

    # Extraire la description du produit
    # Trouver la balise <meta> avec l'attribut name="description"
    description = soup.find("meta", attrs={"name": "description"})
    # Extraire le contenu de l'attribut "content"
    product_description_raw = description.get("content")
    product_description_cleaned = product_description_raw.strip()
    product_description = re.sub(r'[^\x00-\x7F]+', '', product_description_cleaned)
    #product_description = product_description_raw.encode('ascii', 'ignore').decode("utf-8")

    page_info_dict = {
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
    print(page_info_dict)
    return page_info_dict


def write_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category",
                      "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)


def extract_book_image(data):
    image_link = data["image_url"]
    file_name_raw = data["title"]
    category = data["category"]
    file_name_re = re.sub(r'[\\/*?:"<>|]', '_', file_name_raw)
    if len(file_name_re) > 60:
        file_name = file_name_re[:60] + "..."
    else:
        file_name = file_name_re
    print(file_name)
    print(image_link)
   # if not os.path.exists(category):
        #os.makedirs(category)

    # Chemin absolu vers le répertoire du projet
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Chemin absolu vers le dossier "webscraping" dans le répertoire du projet
    webscraping_directory = os.path.join(project_directory, "webscraping")

    images_folder = os.path.join(webscraping_directory, "images")
    # Créer le dossier "images" s'il n'existe pas déjà
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    category_folder = os.path.join(images_folder, category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)



    request = urllib.request.urlopen(image_link)
    img = request.read()
    print(category)
    print(file_name)
    chemin_complet = os.path.join(category_folder, file_name + '.jpg')
    print(chemin_complet)
    with open(chemin_complet, 'wb') as f:
        f.write(img)


url= "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

data = get_book_info(url)
extract_book_image(data)