# Sex Shop
# Práctica 1: 
Esta práctica corresponde a la asignatura _Tipología y ciclo de vida de los datos_ de la Universitat Oberta de Catalunya. Se aplicaran tecnicas de _web scraping_ para extraer datos de 2 paginas Web distintas y combinarlas en un conjunto de datos.
Se puede acceder mediante los siguientes links: 
* **-Desmontando a la Pili** https://desmontandoalapili.com/?v=6b83b0879ce8
* **-Eurovisex** https://eurovisex.com/

## Instalación de dependencias

Para instalar las dependencias necesarias, ejecuta el siguiente comando:

pip install -r requirements.txt

El codigo puede ejecutarse desde el archivo main.py.

Esto iniciara el proceso de Web Scraping en dichas paginas que dara lugar a la creacion de los datasets y la carpeta imagenes_productos dentro de la carpeta **/Data/**.


## DOI de Zenodo
10.5281/zenodo.14042744


## Miembros del equipo

La actividad ha sido realizada de manera conjunta por **Francisco Javier Gonzalez Ontanon** y **Laureano Ezequiel Rios Oriol**.

## Ficheros

* **Source/Scrap_sexshop_DesmontandoLaPili.py**: Contiene el codigo para iniciar el proceso de Web Scraping.
* **Source/Scrap_sexshop_Eurovisex.py**: Contiene el codigo para iniciar el proceso de Web Scraping.
* **Data/productos_desmontandoLaPili.py**: Contiene el Dataset generado.
* **Data/productos_eurovisex.py**: Contiene el Dataset generado.
* **Data/imagenes_productos**: Contiene las iamgenes de cada producto.

## Recursos

1. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
