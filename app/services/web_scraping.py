from bs4 import BeautifulSoup as bs 
import cloudscraper
import json
import re
from urllib.parse import quote
from open_library import search_book_info
from gemini import generate
from pdf_processor import PDFProcessor
from upload_cloudinary import uploadPDF

def search_book(book_title: str):
    # Formatear la URL con el título del libro codificado
    base_url = "https://es.pdfdrive.com/search?q="
    search_url = f"{base_url}{quote(book_title)}&searchin=es&more=true"
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(search_url)
        soup = bs(response.text, 'html.parser')
        
        # Depuración: Imprimir el contenido de soup para verificar la estructura
        # print(soup.prettify())
        
        # Encontrar el primer resultado del libro
        book_item = soup.find('li', {'onclick': lambda x: x and 'ontouchstart' in x})
        if not book_item:
            return None
        
        link = 'https://es.pdfdrive.com' + book_item.find('a', href=True)['href']
        # Extraer detalles del libro
        book_info = {
            'title': book_item.find('h2').text.strip(),
            'image': book_item.find('img')['src'],
            'downloads': download_pdf(link,book_item.find('h2').text.strip()),
        }
        
        # Obtener información adicional
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
        # Agregamos la api de OpenLibrary en caso de que no exista el año y 
        # el autor.
        info_api_library = search_book_info(book_title)
        book_info['author'] = info_api_library['author']
        if book_info['year'] == None or int(book_info['year']) >= int(info_api_library['publication_year']) :
            book_info['year'] = info_api_library['publication_year'] 

        # Para agregar una breve descripcion elegi Gemini Api , en donde hago
        # un prompt sencillo pero eficiente para tener una descripcion sin problemas
        generate_info =  generate(book_title)
        book_info['description'] = generate_info['resumen']
        book_info['category'] = generate_info['categoria']
        return book_info

    except Exception as e:
        return {'error': str(e)}

def scraping(books: list[str]):
    results = []
    for index, book in enumerate(books):
        print(f"Buscando información del libro {index + 1} de {len(books)}: {book}")
        result = search_book(book)
        if result:
            results.append(result)
    return results

def download_pdf(url: str, name: str):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        soup = bs(response.text, 'html.parser')
        download_button = soup.find('button', {'id': 'previewButtonMain'})
        if not download_button:
            return None
        download_link = download_button['data-preview']
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
        processor = PDFProcessor(download_link_pdf)
        pdf_path = processor.download_from_url(download_link_pdf, name)

        return links_dowload
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    result = scraping([
        "Los 7 hábitos de la gente altamente efectiva",
    ])
    print(json.dumps(result, indent=2, ensure_ascii=False))

    