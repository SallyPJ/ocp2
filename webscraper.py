import requests
from bs4 import BeautifulSoup
import csv
import re
from word2number import w2n
import urllib.request
import urllib.parse
import csv
import os



def get_book_info(book_url):
    """
        Retrieves information about a book from the given URL.

        Args:
            book_url (str): The URL of the book page.

        Returns:
            product_data: A dictionary containing information about the book.
        """

    # Retrieve the content of the page and check if the link is active
    try:
        response = requests.get(book_url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the URL of the page
    product_page_url = response.url

    # Extract the title of the book
    product_main_div = soup.find("div", class_="col-sm-6 product_main")
    title_tag = product_main_div.find("h1")
    title = title_tag.get_text()

    # Extract the review rating of the book
    product_info_div = soup.find('div', class_='col-sm-6 product_main')
    rating_paragraph = product_info_div.find('p', class_= lambda x: x and x.startswith('star-rating'))
    rating_class_name = rating_paragraph.get('class')
    rating_letters = rating_class_name[1]
    review_rating = (w2n.word_to_num(rating_letters))

    # Extract the category of the book
    breadcrumb_ul = soup.find("ul", class_="breadcrumb")
    breadcrumb_list_items = breadcrumb_ul.find_all("li")
    category = breadcrumb_list_items[2].text.strip()

    # Extract row content from the table
    table = soup.find('table', class_="table table-striped")
    table_data_tags = table.find_all('td')

    # Initialize variables to store extracted values
    universal_product_code = ""
    price_excluding_tax = ""
    price_including_tax = ""
    number_available = ""

    # Extract data from the selected <td> tags and assign them to variables
    for i, td in enumerate(table_data_tags):
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

    # Extract the partial URL of the book image
    parent_div = soup.find("div", class_="item active")
    img_tag = parent_div.find("img")
    relative_path = img_tag.get("src")
    website_base_url = "https://books.toscrape.com/"
    image_url = urllib.parse.urljoin(website_base_url, relative_path)

    # Extract the description of the book
    description = soup.find("meta", attrs={"name": "description"})
    product_description_raw = description.get("content")
    product_description_cleaned = product_description_raw.strip()
    product_description = re.sub(r'[^\x00-\x7F]+', '', product_description_cleaned)

    # Create a dictionary containing information about the book
    product_data = {
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
    print(product_data)
    return product_data


def write_data_to_csv(product_data, filename):
    """
        Writes product data to a CSV file.

        Args:
            product_data (dict): A dictionary containing information about the product.
            filename (str): The name of the CSV file to write the data to.
        """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category",
                      "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(product_data)


def extract_book_image(product_data):
    """
        Downloads and saves the image associated to the book.

        Args:
            product_data (dict): A dictionary containing information about the product.
        """
    # Extract data from the dictionnary
    image_link = product_data["image_url"]
    file_name_raw = product_data["title"]
    category = product_data["category"]

    # Replace special characters in the title string
    file_name_re = re.sub(r'[\\/*?:"<>|]', '_', file_name_raw)

    # Reduce title length
    if len(file_name_re) > 60:
        file_name = file_name_re[:60] + "..."
    else:
        file_name = file_name_re
    print(file_name)
    print(image_link)

    # Create image/category directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    webscraping_directory = os.path.join(script_directory, "webscraping_booktoscrape")
    images_folder = os.path.join(webscraping_directory, "images")
    category_folder = os.path.join(images_folder, category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    # Open a connection to the image URL and read its content
    image_request = urllib.request.urlopen(image_link)
    image_download = image_request.read()
    print(category)
    print(file_name)
    # Define the complete path where the image will be saved
    image_path = os.path.join(category_folder, file_name + '.jpg')
    print(image_path)
    # Write the downloaded image to the specified file path
    with open(image_path, 'wb') as f:
        f.write(image_download)


book_url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

product_data = get_book_info(book_url)
extract_book_image(product_data)