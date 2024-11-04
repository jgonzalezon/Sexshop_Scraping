import requests
from bs4 import BeautifulSoup
import time
import random
import os
from urllib.parse import urljoin, urlparse
import Scraping.utils
import Scraping.constants



def main():

    # Crear carpeta para las imágenes si no existe
    imagenes_folder = "data/imagenes_productos"
    os.makedirs(imagenes_folder, exist_ok=True)
    
    
    todos_productos = []
    todos_precios = []
    todos_descripciones = []
    todos_imagenes = []
    todas_paginas = []
    
    
    def obtener_descripcion_producto(url_producto):
        try:
            # Realizar la solicitud HTTP
            response = requests.get(url_producto, headers=Scraping.constants.HEADERS)
            response.raise_for_status()
            
            # Parsear el contenido HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar la descripción del producto
            descripcion_tag = soup.find('div', class_='summary entry-summary').find_all('p')
            descripcion = "\n".join([p.text.strip() for p in descripcion_tag]) if descripcion_tag else "No disponible"
            return descripcion
        except requests.RequestException as e:
            print(f"Error al acceder a la página del producto: {e}")
            return "No disponible"

    def scrape_categoria(url_base):
        try:
            # Realizar la solicitud HTTP a la página base para obtener las categorías
            response = requests.get(url_base, headers=Scraping.constants.HEADERS)
            response.raise_for_status()
            
            # Parsear el contenido HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar todas las categorías de productos
            categorias = soup.find('div', id='woocommerce_product_categories-4').find('ul', class_='product-categories').find_all('a')
            
            # Recorrer cada categoría
            for categoria in categorias:
                categoria_url = categoria['href']
                print(f"Scraping categoría: {categoria_url}")
                
                # Scrape de productos en cada categoría
                scrape_productos_categoria(categoria_url)
                
        except requests.RequestException as e:
            print(f"Error al acceder a la página base {url_base}: {e}")
            
            
    

    def scrape_productos_categoria(url_categoria):
        

        page = 1
        while True:
            try:
                # URL de la página actual de la categoría
                url = f"{url_categoria}page/{page}/"
                
                # Realizar la solicitud HTTP con tiempos de espera aleatorios
                response = requests.get(url, headers=Scraping.constants.HEADERS)
                response.raise_for_status()
                
                # Parsear el contenido HTML con BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar todos los productos
                items = soup.find_all('li', class_='product')
                
                # Si no hay más productos, salir del bucle
                if not items:
                    break
                
                # Extraer información de cada producto
                for item in items:
                    # Añadir un tiempo de espera aleatorio entre solicitudes
                    time.sleep(random.uniform(1, 3))
                    
                    # Nombre del producto
                    nombre_tag = item.find('h2', class_='woocommerce-loop-product__title')
                    if not nombre_tag:
                        continue
                    nombre = nombre_tag.text.strip()
                    todos_productos.append(nombre)
                    
                    # Precio del producto
                    precio_tag = item.find('span', class_='woocommerce-Price-amount amount')
                    precio = precio_tag.text.strip().replace('€', '').strip() if precio_tag else "No disponible"
                    todos_precios.append(precio)
                    
                    # URL del producto para obtener la descripción
                    enlace_tag = item.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
                    if enlace_tag:
                        url_producto = enlace_tag['href']
                        descripcion = obtener_descripcion_producto(url_producto)
                    else:
                        descripcion = "No disponible"
                    todos_descripciones.append(descripcion)
                    
                    # Imagen del producto
                    imagen_tag = item.find('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
                    imagen_url = imagen_tag.get('data-src') or imagen_tag.get('src') if imagen_tag else "No disponible"
                    if imagen_url != "No disponible" and urlparse(imagen_url).scheme in ["http", "https"]:
                        imagen_nombre = os.path.join(imagenes_folder, os.path.basename(imagen_url))
                        imagen_response = requests.get(imagen_url, headers=Scraping.constants.HEADERS)
                        if imagen_response.status_code == 200:
                            with open(imagen_nombre, 'wb') as f:
                                f.write(imagen_response.content)
                        todos_imagenes.append(imagen_nombre)
                    else:
                        todos_imagenes.append("No disponible")
                    
                    # Página del producto
                    todas_paginas.append(url)
                
                # Siguiente página
                page += 1

            except requests.RequestException as e:
                print(f"Error al acceder a la página {url}: {e}")
                break
    
    
    
    
    
    # Inicializar listas para guardar los datos
    eurovisex_base_url = "https://eurovisex.com/categoria-producto/womens"
    scrape_categoria(eurovisex_base_url)
    
    Scraping.utils.guardar_datos(todos_productos, todos_precios, todos_descripciones, todos_imagenes, todas_paginas,"data/productos_eurovisex.csv")


if __name__ == "__main__":
    main()

