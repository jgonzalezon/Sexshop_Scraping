import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import os
import csv
import time


# ENCABEZADOS PARA LAS SOLICITUDES
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}

# URL ,NUMERO DE PAGINAS, CARPETA DE IMAGENES Y ARCHIVO CSV
BASE_URL = 'https://www.ferreteriamaranges.com/ferreteria-tagFamFER/?cmd=page&num='
NUM_PAGES = 120
IMAGES_FOLDER = 'images'
CSV_FILE = 'productos.csv'


def create_folder(path):
    """CREAMOS CARPETA"""
    if not os.path.exists(path):
        os.makedirs(path)

def fetch_page(url):
    """Fetch a webpage and return the response content."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return None

def parse_product(product):
    """ANALIZAMOS Y RETORNAMOS LOS VALORES BUSCADOS"""
    try:
        name = product.find('h2', class_='product-name').text.strip()
        price = product.find('span', class_='product-price').text.strip()
        image_url = product.find('img')['src']
        return name, price, image_url
    except AttributeError as e:
        print(f'Error parsing product: {e}')
        return None, None, None

def save_image(image_url, path):
    """GUARDAMOS IMAGEN """
    try:
        image_response = requests.get(image_url)
        with open(path, 'wb') as file:
            file.write(image_response.content)
        print(f'Imagen guardada en: {path}')
    except requests.exceptions.RequestException as e:
        print(f'Error fetching image {image_url}: {e}')

def scrapear_pagina(url, page_num, csv_writer):
    """REALIZAMOS SCRPA EN UNA PAGINA Y VAMOS GUARDANDO EN FICHERO CSV"""
    content = fetch_page(url)
    if content is None:
        return
    
    soup = BeautifulSoup(content, 'html.parser')
    for product in soup.find_all('div', class_='product-item'):
        name, price, image_url = parse_product(product)
        if name and price and image_url:
            image_path = f'{IMAGES_FOLDER}/{page_num}_{name}.jpg'
            save_image(image_url, image_path)
            csv_writer.writerow([name, price, image_path])

def main():
    """FUNCION PRINCIPAL PARA EJECUTAR SCRAP"""
    create_folder(IMAGES_FOLDER)

    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Nombre', 'Precio', 'Ruta de la Imagen'])

        for page in range(1, NUM_PAGES + 1):
            url = f'{BASE_URL}{page}#anchorView'
            print(f'Scrapeando página {page}')
            scrapear_pagina(url, page, csv_writer)
            time.sleep(3)  # RETRASO DE 3 SEGUNDOS PARA NO SATURAR LA PAGINA

    print('Scraping completado.')

if __name__ == "__main__":
    main()
