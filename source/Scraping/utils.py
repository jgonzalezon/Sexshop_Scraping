import pandas as pd # type: ignore
import os

def guardar_datos(productos, precios, descripciones, imagenes, paginas, output_file="data/productos.csv"):
    # Función para guardar el DataFrame en un archivo CSV
    data = {
        'Producto': productos,
        'Precio': precios,
        'Descripcion': descripciones,
        'Imagen': imagenes,
        'Pagina': paginas
    }
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    
    print(df)