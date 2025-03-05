from bs4 import BeautifulSoup as bs 
import requests
import json
import re
from urllib.parse import quote

def search_book_info(book_title: str):
    # Format the URL with the encoded book title
    base_url = "https://es.pdfdrive.com/search?q="
    search_url = f"{base_url}{quote(book_title)}&searchin=es&more=true"
    
    try:
        response = requests.get(search_url)
        soup = bs(response.text, 'html.parser')
        
        # Find the first book result
        book_item = soup.find('li', {'onclick': lambda x: x and 'ontouchstart' in x})
        if not book_item:
            return None
        
        link = 'https://es.pdfdrive.com' + book_item.find('a', href=True)['href']
        # Extract book details
        book_info = {
            'title': book_item.find('h2').text.strip(),
            'link': link,
            'image': book_item.find('img')['src'],
            'downloads': download_pdf(link)
        }
        
        # Get additional info
        file_info = book_item.find('div', class_='file-info')
        if file_info:
            info_spans = file_info.find_all('span')
            for span in info_spans:
                if 'fi-pagecount' in span.get('class', []):
                    book_info['pages'] = span.text.strip()
                elif 'fi-year' in span.get('class', []):
                    book_info['year'] = span.text.strip()
                elif 'fi-size' in span.get('class', []):
                    book_info['size'] = span.text.strip()
                elif 'fi-lang' in span.get('class', []):
                    book_info['language'] = span.text.strip()
        
        return book_info
        
    except Exception as e:
        return {'error': str(e)}

def scraping(books: list[str]):
    results = []
    for book in books:
        result = search_book_info(book)
        if result:
            results.append(result)
    return results

def download_pdf(url: str):
    try:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        download_link = soup.find('button', {'id': 'previewButtonMain'})['data-preview']
        # ebook/preview?id=189551951&session=784f9be7aed4954389ed71f2a18be609
        indent = re.search(r'id=(\d+)&', download_link).group(1)
        session = re.search(r'session=(\w+)', download_link).group(1)
        ext_pdf = "pdf"
        ext_mobi= "mobi"
        ext_epu = "epu"

        download_link_pdf = f"https://es.pdfdrive.com/download.pdf?id={indent}&h={session}&u=cache&ext={ext_pdf}"
        download_link_mobi = f"https://es.pdfdrive.com/download.pdf?id={indent}&h={session}&u=cache&ext={ext_mobi}"
        download_link_epu = f"https://es.pdfdrive.com/download.pdf?id={indent}&h={session}&u=cache&ext={ext_epu}"
       
        links_dowload = {
                "pdf": download_link_pdf,
                "mobi": download_link_mobi,
                "epub": download_link_epu }

        return links_dowload
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    result = search_book_info("elefante")
    pdf_link = download_pdf(result['link'])
    print(pdf_link)
    print(json.dumps(result, indent=2, ensure_ascii=False))


