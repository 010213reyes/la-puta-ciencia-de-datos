# Pipeline ETL con Python y SQLite

## Descripción

Este proyecto implementa un pipeline ETL utilizando Python, Pandas y SQLite.

El proceso toma información de ventas almacenada en un archivo CSV, transforma los datos, crea una nueva variable y los modela mediante un esquema estrella antes de cargarlos en una base de datos SQLite.

## Tecnologías

* Python
* Pandas
* SQLite
* Git
* GitHub

## Estructura del proyecto

```text
practica-etl/
├── ventas.csv
├── etl.py
├── README.md
└── almacen.db
```

## 1. EXTRACT

La primera fase lee el archivo `ventas.csv` utilizando Pandas.

El archivo contiene las siguientes columnas:

* `producto`
* `categoria`
* `precio`
* `cantidad`

Los datos se cargan en un DataFrame para poder procesarlos.

## 2. TRANSFORM

Durante esta fase se crea una nueva variable llamada `total`.

La variable se calcula mediante:

```text
total = precio × cantidad
```

Esta variable representa el ingreso correspondiente a cada registro de venta.

También se construye un esquema estrella simplificado compuesto por:

### dim_categoria

Contiene las categorías de productos y un identificador `cat_id`.

### fact_ventas

Contiene los datos de las ventas y utiliza `cat_id` para relacionarse con la dimensión de categorías.

La estructura permite separar las dimensiones descriptivas de los datos numéricos utilizados para el análisis.

## 3. LOAD

En la última fase se utiliza SQLite para almacenar los datos transformados.

Se crean dos tablas:

* `dim_categoria`
* `fact_ventas`

La base de datos generada es `almacen.db`.

## Consulta analítica

Finalmente se ejecuta una consulta SQL que relaciona la tabla de hechos con la dimensión mediante `JOIN`.

La consulta agrupa las ventas por categoría y calcula:

* Número de ventas.
* Ingresos totales.

Esto permite comprobar que el esquema estrella puede utilizarse para realizar consultas analíticas.

## Ejecución

Para ejecutar el proyecto:

```bash
python etl.py
```

## Resultado

El programa muestra en la terminal las etapas de extracción, transformación y carga, además del resultado de la consulta analítica final.
