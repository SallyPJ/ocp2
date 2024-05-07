import requests
from bs4 import BeautifulSoup
import re
from word2number import w2n
from urllib.request import urlopen
import urllib.parse
import csv
import os

website_url = "https://books.toscrape.com/index.html"
category_urls_dict = {}


def get_book_info(book_url):
    """
    Retrieves information about a book from the given URL.

    Args:
        book_url (str): The URL of the book page.

    Returns:
        product_data (dict): A dictionary containing information about the book.
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

    try:
        with urlopen(image_link) as response :
            # Open a connection to the image URL and read its content
            image = response.read()
            # Define the complete path where the image will be saved
            image_path = os.path.join(category_folder, file_name + '.jpg')
            print(image_path)
            with open(image_path, "wb") as f:
                f.write(image)

    except Exception as e :
        print(f"Error downloading image: {e}")

def retrieve_category_url(website_url):
    """
    Retrieve category names and URLs from the main page.

    Args:
        website_url (str): the url of book_toscrape main page.
    """
    # Retrieve the content of the page and parse the HTLM
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the navigation list element containing category links
    navigation_list = soup.find("ul", class_="nav nav-list")
    list_items = navigation_list.find_all("li")

    # Initialize a dictionary to store category names and URLs
    result ={"category_name": [],"category_url": []}

    # Base url to concatenate with category href
    cat_base_url = "https://books.toscrape.com/"

    for list_item in list_items:
        # Extract category main page url
        category_href_index = list_item.find("a").get("href")
        category_partial_url = category_href_index.replace("index.html", "")

        # Extract the category name and append it to the list
        category_name = list_item.find("a").text.strip()
        result["category_name"].append(category_name)

        # Construct the category page URL and append it to the list
        category_url = urllib.parse.urljoin(cat_base_url, category_partial_url)
        result["category_url"].append(category_url)

    # Remove the first element from both lists (header)
    del result["category_name"][0]
    del result["category_url"][0]

    # Create a dictionary entry with category names as keys and URLs as values
    for category_name, category_url in zip(result["category_name"], result["category_url"]):
        # Create dictionary containing a sub-key "category_main_url" with the URL as the value.
        category_urls_dict[category_name] = {"category_main_url": category_url}
    print(category_urls_dict)
    return category_urls_dict


def extract_all_page_urls_by_category(category_urls_dict):
    """
    Extract all page URLs by category and add them to a subdictionnary in category_urls_dict.

    Args:
        category_urls_dict (dict): the dictionnary which contains main page url for each category

    Returns :
        category_urls_dict["urls_list_by_category"] (dict) : A subdictionnary with url pages listed by category
    """

    # Iterate through each category and its data in the dictionary
    for category, category_data in category_urls_dict.items():
        # Extract the main URL for each category
        category_main_url = category_data["category_main_url"]
        print(category_main_url)

        # Send a request to fetch the category main URL and parse the HTML
        response = requests.get(category_main_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Initialize a list to store URLs per category
        urls_list_by_category = []
        urls_list_by_category.append(category_main_url)

        # Find the next button to navigate through pages
        next_button = soup.find("li", class_="next")
        while next_button:
            # Extract the URL of the next page
            next_partial_url = next_button.find("a").get("href")
            next_full_url = urllib.parse.urljoin(category_main_url, next_partial_url)
            urls_list_by_category.append(next_full_url)

            # Send a request to fetch the next page and parse the HTML
            response = requests.get(next_full_url)
            soup = BeautifulSoup(response.text, "html.parser")
            next_button = soup.find("li", class_="next")

        # If there's no next button, print a message
        if not next_button:
            print("Il n'y a plus de bouton 'next'.")
        print(urls_list_by_category)

        # Add the list of url pages of a category to a dedicated subdictionnary in category_urls_dict
        category_urls_dict.setdefault(category,{})["urls_list_by_category"] = urls_list_by_category


    print(category_urls_dict)

    return category_urls_dict


def retrieve_book_urls(category_urls_dict):
    """
    Extract all the books url from each page of a category.

    Args:
        category_urls_dict (dict): The dictionnary which contains all pages urls for each category

    """
    for category,category_data in category_urls_dict.items():
        # Extract the URLs list for the current category
        category_urls = category_data["urls_list_by_category"]
        books_urls = []

        #Base URL for for books to concatenate with books href
        book_base_url = "https://books.toscrape.com/catalogue/"

        # Iterate through each URL in the category URLs list
        for url in category_urls:
            # Fetch the webpage content for the current URL
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all articles with class "product_pod"
            product_articles = soup.find_all("article", class_="product_pod")
            for article in product_articles:
                book_h3_tag = article.find("h3")
                book_link = book_h3_tag.find("a").get("href")

                # Split the URL by '/' to extract the partial URL
                parts = book_link.split('/')
                book_partial_url = parts[-2] + '/' + parts[-1]

                # Join the partial URL with the base URL to get the full URL
                book_full_url = urllib.parse.urljoin(book_base_url, book_partial_url)
                books_urls.append(book_full_url)

        # Assign the list of books URLs to the corresponding category data in the dictionnary
        category_data["books_url"] = books_urls
        print(category_data["books_url"])




def scrap_books_by_category(category_urls_dict):
    """
    Extract all the books data by category, print csv list by category and download images for each books.

    Args:
        category_urls_dict (dict): The dictionnary which contains all books urls for each category

    """
    # Obtaining the absolute path to the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Obtaining the absolute path to the "webscraping" folder within the project directory
    folder_name = os.path.join(project_directory, "webscraping_booktoscrape")

    # Creating the folder if it doesn't already exist
    os.makedirs(folder_name, exist_ok=True)

    # Iterating through each category and its book url list
    for category,category_data in category_urls_dict.items():
        # Retrieving the list of books URLs for the current category
        list_of_books_url = category_data["books_url"]

        # Initializing an empty list to store all book data for the current category
        all_data = []

        # Iterating through each book URL in the list
        for book in list_of_books_url:
            # Obtaining data for the current book
            data = get_book_info(book)

            # Extracting and downloading the book image
            extract_book_image(data)

            # Appending the book data to the list of all data for the current category
            all_data.append(data)

        # Constructing the filename for the CSV file based on the category
        csv_filename = os.path.join(folder_name, f"{category}.csv")

        # Writing the collected book data to a CSV file
        write_to_csv(all_data, csv_filename)


def write_to_csv(data_list, filename):
    """
    Write data to a CSV file.

    Args:
        data_list (list): List of dictionaries containing the data to be written.
        filename (str): The name of the CSV file to write to.
    """
    # Open the CSV file in write mode with UTF-8 encoding
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        # Define the field names for the CSV header
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category",
                      "review_rating", "image_url"]
        # Create a CSV writer object with the defined field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the CSV header
        writer.writeheader()
        # Iterate through each dictionary in the data list
        for data in data_list:
            # Write the data to the CSV file
            writer.writerow(data)

category_urls_dict = retrieve_category_url(website_url)
extract_all_page_urls_by_category(category_urls_dict)
retrieve_book_urls(category_urls_dict)
scrap_books_by_category(category_urls_dict)


