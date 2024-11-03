import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from urllib.parse import urljoin, urlparse

# Cambiar el 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}

# Crear carpeta para las imágenes si no existe
imagenes_folder = "imagenes_productos"
os.makedirs(imagenes_folder, exist_ok=True)

# Inicializar listas para guardar los datos
todos_productos = []
todos_precios = []
todos_descripciones = []
todos_imagenes = []
todas_paginas = []

def obtener_descripcion_producto(url_producto):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(url_producto, headers=HEADERS)
        response.raise_for_status()
        
        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar la descripción del producto
        descripcion_tag = soup.find('div', class_='woocommerce-product-details__short-description')
        descripcion = descripcion_tag.text.strip() if descripcion_tag else "No disponible"
        return descripcion
    except requests.RequestException as e:
        print(f"Error al acceder a la página del producto: {e}")
        return "No disponible"

def scrape_categoria(url_base, paginas):
    for page in range(1, paginas + 1):
        try:
            # URL de la página actual
            url = f"{url_base}/page/{page}"

            # Realizar la solicitud HTTP con tiempos de espera aleatorios
            response = requests.get(url, headers=HEADERS)

            # Comprobar si la solicitud fue exitosa
            response.raise_for_status()

            # Parsear el contenido HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscar todos los productos
            items = soup.find_all('li', class_='product')
            
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
                precio = precio_tag.text.strip() if precio_tag else "No disponible"
                todos_precios.append(precio)
                
                # URL del producto para obtener la descripción
                enlace_tag = item.find('a', class_='woocommerce-LoopProduct-link')
                if enlace_tag:
                    url_producto = enlace_tag['href']
                    descripcion = obtener_descripcion_producto(url_producto)
                else:
                    descripcion = "No disponible"
                todos_descripciones.append(descripcion)
                
                # Imagen del producto
                imagen_container = item.find('div', class_='inside-wc-product-image')
                if imagen_container:
                    imagen_tag = imagen_container.find('img')
                    # Priorizar data-src si existe, en caso contrario usar src
                    imagen_url = imagen_tag.get('data-src') or imagen_tag.get('src') if imagen_tag else "No disponible"
                    if imagen_url != "No disponible" and urlparse(imagen_url).scheme in ["http", "https"]:
                        imagen_nombre = os.path.join(imagenes_folder, os.path.basename(imagen_url))
                        imagen_response = requests.get(imagen_url, headers=HEADERS)
                        if imagen_response.status_code == 200:
                            with open(imagen_nombre, 'wb') as f:
                                f.write(imagen_response.content)
                        todos_imagenes.append(imagen_nombre)
                    else:
                        todos_imagenes.append("No disponible")
                else:
                    todos_imagenes.append("No disponible")
                
                # Página del producto
                todas_paginas.append(url)

        except requests.RequestException as e:
            print(f"Error al acceder a la página {page}: {e}")

# Scrape de la categoría 'jugar'
scrape_categoria("https://desmontandoalapili.com/categoria-producto/jugar", 10)

# Scrape de la categoría 'bienestar'
scrape_categoria("https://desmontandoalapili.com/categoria-producto/bienestar", 3)


# ----------------------------------------------TODO--------------------------------------------------
# Replicar código ya existente.

# Scrape de la página: https://eurovisex.com/tienda/
# Scrape de la página: https://insinuat.com/es/21-juguetes (Scrapear todas las categorías, quizás el programa pueda navegar entre ellas)
# Scrape de la página: https://miconsolador.es/consoladores-480?p=2
# Scrape de la página: (Revisar más páginas de tiendas de Zaragoza y alguna online grande como platano melón)

# Guardar los datos en un DataFrame de Pandas
data = {
    'Producto': todos_productos,
    'Precio': todos_precios,
    'Descripcion': todos_descripciones,
    'Imagen': todos_imagenes,
    'Pagina': todas_paginas
}
df = pd.DataFrame(data)

# Exportar el DataFrame a un archivo CSV
output_file = "productos_jugar.csv"
df.to_csv(output_file, index=False, sep=';', encoding='utf-8', line_terminator='')

# Mostrar el DataFrame 
print(df)
