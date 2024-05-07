
import webscraper



if __name__ == '__main__':
    category_urls_dict = webscraper.retrieve_category_url(website_url)
    webscraper.extract_all_page_urls_by_category(category_urls_dict)
    webscraper.retrieve_book_urls(category_urls_dict)
    webscraper.scrap_books_by_category(category_urls_dict)
