# Projet 2 : Web Scraping of books.toscrape.com

## Description
This web scraping project is designed to extract information about categories and books from the website [books.toscrape](https://books.toscrape.com/index.html).   
The script generates CSV files for each category, containing detailed information about the books within that category, and stores book images in dedicated folders.
## Dependencies
- **beautifulsoup4**  
- **requests**  
- **word2number**  
## Features
- Collect the URLs of each category :  **get_category_urls(website_url)**
- Retrieve information about books within a given category, write a csv file for each category and download the image associated with each book : **scrape_books_and_images(category_url)**
- Extract data from a book page such as product page URL, title, review rating, category, universal product code, price, availability, product description, and image URL : **get_book_info(book_url)**

## Installation ##
### 1. Prerequisites
Before installing the program, ensure that you have Python installed on your system. You can download and install Python from the official website: Python Downloads.
### 2. Clone the project
To get started, you'll need to clone the project repository onto your local machine. Follow these steps:
- Open Git Bash or your preferred terminal application.
- Navigate to the directory where you want to clone the project using the cd (change directory) command. 
- Run the following command to clone the repository:
 ```bash
  git clone https://github.com/SallyPJ/ocp2.git
```
### 3. Create and activate a virtual environment in the project folder
 In the project folder, create the virtual environment.  
 ```bash
python -m venv env
```
Then activate the project environment.  
Windows(Powershell)
```bash
source env\scripts\activate 
```
Linux/Mac
```bash
source env/bin/activate
```
### 4. Install dependencies
The program relies on several Python libraries which can be installed using pip. Navigate to the directory containing the project files in your terminal or command prompt and run the following command:

 ```bash
pip install -r requirements.txt
```
### 5. Run the program
 ```bash
python main.py
```
## Outputs
- Output directory structure
 ```bash
output_folder/
│
├── category_1/
│   ├── category_1.csv
│   ├── images_category_1/
│   │   ├── book1_image.jpg
│   │   ├── book2_image.jpg
│   │   └── ...
│
├── category_2/
│   ├── category_2.csv
│   ├── images_category_2/
│   │   ├── book1_image.jpg
│   │   ├── book2_image.jpg
│   │   └── ...
│
└── ...
```
- Example of extracted data
```bash
{'product_page_url': 'https://books.toscrape.com/catalogue/see-america-a-celebration-of-our-national-parks-treasured-sites_732/index.html',
'universal_product_code': 'f9705c362f070608',
'title': 'See America_ A Celebration of Our National Parks & Treasured Sites',
'price_including_tax': '48.87',
'price_excluding_tax': '48.87',
'number_available': 14,
'product_description': "To coincide with the 2016 centennial anniversary of the National Parks Service, the Creative Action Network has partnered with the National Parks Conservation Association to revive and reimagine the legacy of WPA travel posters. Artists from all over the world have participated in the creation of this new, crowdsourced collection of See America posters for a modern era. Fe To coincide with the 2016 centennial anniversary of the National Parks Service, the Creative Action Network has partnered with the National Parks Conservation Association to revive and reimagine the legacy of WPA travel posters. Artists from all over the world have participated in the creation of this new, crowdsourced collection of See America posters for a modern era. Featuring artwork for 75 national parks and monuments across all 50 states, this engaging keepsake volume celebrates the full range of our nation's landmarks and treasured wilderness. ...more",  
'category': 'Travel',
'review_rating': 3,
'image_url': 'https://books.toscrape.com/media/cache/c7/1a/c71a85dbf8c2dbc75cb271026618477c.jpg'}
```
- Example of book data listed in a CSV file
![image](https://github.com/SallyPJ/ocp2/assets/166709267/683a50e5-fdbb-4334-b112-c1df30dc93f4)


## Licence ##
MIT License
