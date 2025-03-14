import requests
from urllib.parse import quote

def search_book_info(book_name):
    link = f"https://openlibrary.org/search.json?title={quote(book_name)}&lang=esp&limit=1"
    response = requests.get(link)

    if response.status_code == 200:
        data = response.json()
        
        book_info = {}
        if data.get('docs') and len(data['docs']) > 0:
            book = data['docs'][0]
            if 'author_name' in book and len(book['author_name']) > 0:
                book_info['author'] = book['author_name'][0]
            if 'first_publish_year' in book:
                book_info['publication_year'] = book['first_publish_year']
        return book_info
    else:
        print(f'Error: {response.status_code}')
   

