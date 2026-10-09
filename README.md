# ETLconPythonV1

Pipeline ETL que procesa datos de e-commerce para generar métricas de ventas.

# ETL E-commerce con Python y Pandas

## 1. Descripción del proyecto

Este proyecto consiste en el desarrollo de una pipeline ETL (*Extract, Transform, Load*) utilizando Python y Pandas para procesar datos de un sistema de comercio electrónico.

El objetivo es extraer información de diferentes archivos CSV, explorar y limpiar los datos, corregir sus tipos, realizar análisis orientados al negocio y exportar los resultados en formatos adecuados para su posterior utilización.

## Objetivos

* Construir una pipeline ETL utilizando Python y Pandas.
* Explorar la estructura y calidad de los datos de un e-commerce.
* Identificar y tratar valores nulos.
* Detectar y eliminar registros duplicados.
* Corregir tipos de datos para facilitar su procesamiento.
* Responder preguntas de negocio mediante agregaciones.
* Exportar los resultados en CSV y Parquet.
* Documentar el proceso y las decisiones de transformación.

### Instalación de dependencias

Para ejecutar el proyecto se necesita Python y las siguientes bibliotecas:

```bash
pip install pandas pyarrow
```

Los módulos `glob` y `os` forman parte de la biblioteca estándar de Python, por lo que no requieren instalación adicional.

## 2. Estructura del proyecto

La estructura utilizada durante el desarrollo es la siguiente:

```text
etl-ecomm/
├── data/
│   ├── ecommerce_orders.csv
│   ├── ecommerce_order_items.csv
│   ├── ecommerce_customers.csv
│   ├── ecommerce_products.csv
│   ├── ecommerce_categories.csv
│   ├── ecommerce_brands.csv
│   ├── ecommerce_inventory.csv
│   ├── ecommerce_promotions.csv
│   ├── ecommerce_reviews.csv
│   ├── ecommerce_suppliers.csv
│   └── ecommerce_warehouses.csv
├── output/
│   ├── orders_clean.csv
│   ├── orders_clean.parquet
│   ├── ventas_por_cliente.csv
│   └── ventas_por_mes.csv
└── etl.py
```

La carpeta `data/` contiene los archivos originales descargados. Durante esta primera versión, la extracción y los análisis se concentran principalmente en cuatro tablas: `orders`, `order_items`, `customers` y `products`.

La carpeta `output/` almacena los archivos generados durante la ejecución. Se crea automáticamente si no existe.

## 3. Arquitectura ETL

El proceso se divide conceptualmente en tres etapas:

* **Extract:** lectura de los archivos de origen.
* **Transform:** exploración, limpieza, corrección de tipos y análisis.
* **Load:** exportación de los resultados a CSV y Parquet.

## 4. Detección de valores nulos

La función `check_nulls()` recorre las cuatro tablas y muestra dos métricas por columna:

```python
df.isnull().sum()
```

Cuenta la cantidad de valores faltantes.

```python
(df.isnull().mean() * 100).round(2)
```

Calcula el porcentaje de valores faltantes respecto del total de filas.

Para calcular ese porcentaje, Pandas interpreta los valores nulos como `True` al aplicar `isnull()`, y el promedio de valores booleanos equivale a la proporción de valores faltantes. Al multiplicar por 100, se obtiene el porcentaje.

Por ejemplo, si una columna tiene 100 registros y 10 son nulos, el porcentaje de valores faltantes es del 10 %.

### ¿Por qué analizar los nulos antes de eliminarlos?

No todos los valores nulos representan errores. Su significado depende de la columna y de las reglas del negocio.

Por ejemplo:

* Un `customer_id` faltante impide identificar al cliente de un pedido.
* Un `total_amount` faltante impide calcular el importe de ese pedido.
* Un `promotion_id` faltante podría indicar que no se utilizó una promoción.
* Un campo `notes` vacío puede ser completamente válido si el cliente no dejó comentarios.

Por este motivo, la estrategia de limpieza debe basarse en el significado de los datos y no únicamente en un porcentaje de valores faltantes.

## 5. Detección y eliminación de duplicados

Los registros duplicados pueden originarse por errores en los datos de origen, cargas repetidas o problemas en los procesos que generan los archivos.

En este proyecto se realizan dos comprobaciones diferentes: duplicados exactos y duplicados por identificador de pedido.

## 6. Corrección de tipos de datos

La corrección de tipos permite que cada columna tenga una representación adecuada para sus operaciones posteriores.

Por ejemplo, una fecha almacenada como texto no permite utilizar directamente todas las funcionalidades temporales de Pandas. Convertirla a un tipo de fecha permite extraer años y meses, ordenar cronológicamente y agrupar ventas por período.

## 7. Análisis de negocio

Una vez realizadas las transformaciones, se utilizan los datos para responder tres preguntas habituales en un negocio de comercio electrónico.

El análisis se implementa mediante agrupaciones, agregaciones y ordenamientos con Pandas.

## 8. Exportación de resultados

La etapa de carga guarda los datos procesados y las métricas de negocio en archivos que pueden reutilizarse en otros análisis.

### Creación del directorio de salida

`os.makedirs()` crea el directorio de salida si no existe.

El parámetro `exist_ok=True` evita que el programa genere un error simplemente porque la carpeta ya existe.

### Exportación a CSV

Los resultados se exportan mediante `to_csv()`.

Se generan tres archivos CSV:

* `ventas_por_cliente.csv`: métricas de gasto y cantidad de órdenes por cliente.
* `ventas_por_mes.csv`: suma mensual de ventas.
* `orders_clean.csv`: tabla de pedidos después de las transformaciones aplicadas.

## 9. Exportación a Parquet

La tabla limpia también se guarda en formato Parquet.

Parquet es un formato de almacenamiento columnar diseñado para trabajar de forma eficiente con datos tabulares.

A diferencia de CSV, conserva metadatos de tipos de datos y suele ofrecer una buena relación entre tamaño de almacenamiento y rendimiento de lectura, especialmente en procesos analíticos.

## 10. Resultados finales

La primera versión de la pipeline permite:

* Extraer cuatro tablas principales desde archivos CSV.
* Explorar la estructura y calidad de los datos.
* Identificar valores faltantes en distintas tablas.
* Eliminar pedidos sin identificador de cliente o importe total.
* Detectar duplicados exactos y por identificador de pedido.
* Corregir los tipos de fecha, importe e identificador de cliente.
* Identificar los cinco clientes con mayor gasto acumulado.
* Calcular los productos con mayor cantidad de unidades vendidas.
* Agrupar las ventas por mes.
* Exportar datos y métricas en CSV y Parquet.

## 11. Limitaciones y mejoras futuras

Esta versión cumple el objetivo de practicar las etapas fundamentales de un ETL, pero existen oportunidades para mejorar su robustez y mantenibilidad.

### Calidad y validación de datos

* Definir reglas de limpieza específicas para cada tabla.
* Revisar los valores nulos generados durante las conversiones de tipos.
* Investigar pedidos con el mismo `order_id` y datos contradictorios.
* Verificar si las cantidades de productos son válidas y si los importes tienen sentido.
* Investigar el pico de ventas de abril de 2025.

### Integridad entre tablas

* Aplicar limpieza a `order_items`.
* Comprobar que los `order_id` de los detalles correspondan a pedidos existentes.
* Comprobar que los `product_id` correspondan a productos válidos.
* Incorporar los nombres de los productos mediante una unión con `products`.

### Análisis de negocio

* Definir qué estados de pedido deben incluirse en las métricas de ventas.
* Revisar si los importes corresponden a ventas confirmadas o a pedidos que luego pueden cancelarse.
* Calcular variaciones porcentuales de ventas entre meses.
* Completar los períodos sin ventas cuando sea apropiado.
* Incorporar análisis de margen, frecuencia de compra y segmentación de clientes.

### Arquitectura y mantenimiento

* Eliminar verificaciones de archivos redundantes.
* Separar la extracción, transformación y carga en funciones claramente definidas.
* Centralizar las rutas y los parámetros de configuración.
* Incorporar validaciones automáticas para verificar la calidad de los resultados.
* Agregar registros de ejecución y manejo de errores.
* Permitir ejecutar el proceso de forma repetible sin alterar los datos originales.

Estas mejoras se abordarán en una segunda versión, con el objetivo de reducir redundancias, mejorar la organización del código y reforzar la confiabilidad de la pipeline.
