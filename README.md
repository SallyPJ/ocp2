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
- Retrieve information about books within a given category, write a csv file for each category and download the image associated with each book : **get_category_info(category_url)**
- Extract data from a book page such as product page URL, title, review rating, category, universal product code, price, availability, product description, and image URL : **get_book_info(book_url)**

## Installation ##
### 1. Prerequisites
Before installing the program, ensure that you have Python installed on your system. You can download and install Python from the official website: Python Downloads.
### 2. Clone the project
To get started, you'll need to clone the project repository onto your local machine. Follow these steps:
- Open Git Bash or your preferred terminal application.
- Run the following command to clone the repository:
 ```bash
  git clone https://github.com/SallyPJ/ocp2.git
```
### 3. Create and activate a virtual environment in the project folder
 In the project folder, create the virtual environment.  
 '''bash
python -m venv env
'''
Then activate the project environment.  
Windows
'''bash
env\Scripts\activate 
'''
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

- Example of book data listed in a CSV file
![image](https://github.com/SallyPJ/ocp2/assets/166709267/31b3d871-27c8-4932-b1d9-a81f8d5ca7b7)

## Licence ##
MIT License
