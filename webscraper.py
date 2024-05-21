import requests
from bs4 import BeautifulSoup
from word2number import w2n
import re
import urllib.parse
import csv
import os


def get_category_urls(website_url):
    """
    Retrieve category URLs from the main page nav bar.

    Args:
        website_url (str): the url of the website main page.
    """
    # Create a session object
    session = requests.session()

    # Retrieve the content of the page and parse the HTML page
    response = session.get(website_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the navigation list element containing category links
    navigation_list = soup.find("ul", class_="nav nav-list").find_all("li")

    # Delete the "Book" category
    del navigation_list[0]

    # Concatenate website URL and retrieved category url
    for list_item in navigation_list:
        # Extract category main page url
        category_partial_url = list_item.find("a").get("href")

        # Construct the category page URL and append it to the list
        category_url = urllib.parse.urljoin(website_url, category_partial_url)

        scrape_books_and_images(session, category_url)


def scrape_books_and_images(session, category_url):
    """
    Retrieves information about books in a given category.

    Args:
        session (requests.Session): The session object to use for making requests.
        category_url (str): The URL of the category page.

    """
    response = session.get(category_url)
    soup = BeautifulSoup(response.text, "html.parser")
    category_name = soup.find("h1").string

    # Create a path to the "webscraping" folder within the project directory
    folders = os.path.join("webscraping_data", category_name, "images")

    # Creating the folder if it doesn't already exist
    os.makedirs(folders, exist_ok=True)

    # Open the CSV file in write mode with UTF-8 encoding
    with open(
            "webscraping_data/" + category_name + "/" + category_name + ".csv",
            "w",
            newline="",
            encoding="utf-8"
    ) as csvfile:
        # Define the field names for the CSV header
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category",
                      "review_rating", "image_url"]
        # Create a CSV writer object with the defined field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the CSV header
        writer.writeheader()

        # Scrape the book classes of the page
        books_class = soup.find_all("article", class_="product_pod")

        # Find the next button to navigate through pages
        next_button = soup.find("li", class_="next")

        while next_button:
            # Extract the URL of the next page
            next_partial_url = next_button.find("a").get("href")
            next_full_url = urllib.parse.urljoin(category_url, next_partial_url)

            # Send a request to fetch the next page and parse the HTML
            response = session.get(next_full_url)
            soup = BeautifulSoup(response.text, "html.parser")
            books_class.extend(soup.find_all("article", class_="product_pod"))
            next_button = soup.find("li", class_="next")

        for book in books_class:
            # Get href to recreate an url for each book
            books_href = book.find("h3").find("a").get("href")
            books_url = urllib.parse.urljoin(category_url, books_href)
            book_info = get_book_info(session, books_url)

            # Write a row for each book
            writer.writerow(book_info)

            # Get book title, upc and image url
            image_url = book_info["image_url"]
            image_upc = book_info["universal_product_code"]
            image_title_raw = book_info["title"]
            # Replace special characters in the title by an underscore
            image_title = re.sub(r'[\\/*?:"<>|]', "_", image_title_raw)

            # Reduce title length
            if len(image_title) > 60:
                image_title = image_title[:60] + "..."

            # Get and download image
            response = session.get(image_url)
            with open(
                    "webscraping_data/" + category_name + "/images/" + image_upc + "_" + image_title + ".jpg",
                    "wb"
            ) as f:
                f.write(response.content)


def get_book_info(session, book_url):
    """
    Retrieves information about a book from the given URL.

    Args:
        session (requests.Session): The session object to use for making requests.
        book_url (str): The URL of the book page.

    Returns:
        product_data (dict): A dictionary containing information about the book.
    """

    # Retrieve the content of the page and check if the link is active
    try:
        response = session.get(book_url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the URL of the page
    product_page_url = response.url

    # Extract the title of the book
    title_raw = soup.find("div", class_="col-sm-6 product_main").find("h1").get_text()

    # Replace non ASCII characters by an underscore
    title = re.sub(r"[^\x00-\x7F]+", "_", title_raw)

    # Extract the review rating of the book
    rating_text = (
        soup.find("div", class_="col-sm-6 product_main")
        .find("p", class_=lambda x: x and x.startswith("star-rating"))
        .get("class")[1]
    )
    review_rating = w2n.word_to_num(rating_text)

    # Extract the category of the book
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

    # Extract row content from the table
    table = soup.find("table", class_="table table-striped")
    table_data_tags = table.find_all("td")

    # Initialize variables to store extracted values
    universal_product_code = ""
    price_excluding_tax = ""
    price_including_tax = ""
    number_available = ""

    # Extract data (book code, price and availability) from the selected <td> tags and assign them to variables
    for i, td in enumerate(table_data_tags):
        text = td.text.strip()
        if i == 0:
            universal_product_code = text
        elif i == 2:
            price_excluding_tax = text.split("£")[1]
        elif i == 3:
            price_including_tax = text.split("£")[1]
        elif i == 5:
            number_available = int(re.findall(r"\d+", text)[0])
        else:
            pass

    # Extract the partial URL of the book image and combine it with the website base url
    image_partial_url = soup.find("div", class_="item active").find("img").get("src")
    image_url = urllib.parse.urljoin("https://books.toscrape.com/", image_partial_url)

    # Extract the description of the book
    product_description_raw = soup.find("meta", attrs={"name": "description"}).get("content").strip()
    # Replace non ASCII characters
    product_description = re.sub(r'[^\x00-\x7F]+', '_', product_description_raw)

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
