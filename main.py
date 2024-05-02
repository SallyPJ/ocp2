
from scrapers import book_info

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

def main (url) :
    page_info = book_info.get_book_info(url)
    if page_info:
        book_info.write_to_csv(page_info, "product_info.csv")
    else:
        print("Les informations du livre n'ont pas pu être récupérées.")

if __name__ == '__main__':

    main(url)