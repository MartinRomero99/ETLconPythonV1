import pandas as pd
import glob
import os

# Verificar que existen los archivos CSV descargados
archivos = glob.glob('etl-ecomm/data/ecommerce_*.csv')
if not archivos:
    print(" No se encontraron los archivos. Asegurate de descargarlos en la carpeta data/")
    print("   Deberías tener: ecommerce_orders.csv, ecommerce_customers.csv, etc.")
else:
    print(f" Archivos encontrados: {len(archivos)}")
    for f in sorted(archivos):
        print(f"  - {os.path.basename(f)}")
# Cargar los CSVs principales
def extract():
    df_orders = pd.read_csv('etl-ecomm/data/ecommerce_orders.csv')
    df_order_items = pd.read_csv('etl-ecomm/data/ecommerce_order_items.csv')
    df_customers = pd.read_csv('etl-ecomm/data/ecommerce_customers.csv')
    df_products = pd.read_csv('etl-ecomm/data/ecommerce_products.csv')
    return df_orders, df_order_items, df_customers, df_products

# Explorar
def explore(df_orders, df_order_items, df_customers, df_products):
    print(f"\n Resumen:")
    print(f"Orders: {len(df_orders)} filas, {len(df_orders.columns)} columnas")
    print(f"Order Items: {len(df_order_items)} filas")
    print(f"Customers: {len(df_customers)} filas")
    print(f"Products: {len(df_products)} filas")
    print()
    print("\n Primeras filas de orders:")
    print(df_orders.head())
    print()
    print("\n Info de orders:")
    print(df_orders.info())
    print()
    # Ver nulos por columna
    print("Nulos por columna:")
    print(df_orders.isnull().sum())
    print()
    

def check_nulls(df_orders, df_order_items, df_customers, df_products):
    tablas = {
        'orders': df_orders,
        'order_items': df_order_items,
        'customers': df_customers,
        'products': df_products
    }

    for nombre, df in tablas.items():
        print(f"\nNulos en {nombre}:")
        print(df.isnull().sum())

        print(f"\nPorcentaje de nulos en {nombre}:")
        print((df.isnull().mean() * 100).round(2))


# Verificar archivos
archivos = glob.glob('etl-ecomm/data/ecommerce_*.csv')
if not archivos:
    print("No se encontraron los archivos CSV.")
else:
    print(f"Archivos encontrados: {len(archivos)}")
    for archivo in sorted(archivos):
        print(f" - {os.path.basename(archivo)}")

    # Ejecutar extracción y exploración
    df_orders, df_order_items, df_customers, df_products = extract()
    explore(df_orders, df_order_items, df_customers, df_products)
    check_nulls(df_orders, df_order_items, df_customers, df_products)

def check_duplicates(df):
    duplicados = df.duplicated().sum()
    print(f"\nDuplicados exactos: {duplicados}")

    duplicados_id = df.duplicated(subset=['order_id']).sum()
    print(f"Order IDs duplicados: {duplicados_id}")


def handle_nulls(df):
    print("\nManejando nulos en orders...")

    antes = len(df)

    df = df.dropna(subset=['customer_id', 'total_amount'])

    print(f"Filas antes: {antes}")
    print(f"Filas eliminadas: {antes - len(df)}")
    print(f"Filas despues: {len(df)}")

    return df

df_orders = handle_nulls(df_orders)
check_duplicates(df_orders)

def remove_duplicates(df):
    print("\nEliminando duplicados...")
    antes = len(df)

    # Eliminar filas exactamente iguales
    df = df.drop_duplicates()
    print(f"Duplicados exactos eliminados: {antes - len(df)}")
    # Ordenar por fecha y conservar un registro por order_id
    df = df.sort_values('order_date')
    df = df.drop_duplicates(subset=['order_id'], keep='last')
    print(f"Filas finales despues de eliminar duplicados: {len(df)}")
    return df
df_orders = remove_duplicates(df_orders)

def correct_types(df):
    print("\nCorrigiendo tipos de datos...")
    print("\nTipos antes de la conversion:")
    print(df.dtypes)

    # Convertir fecha a datetime
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    # Convertir importes a valores numéricos
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
    # Convertir identificador a entero que admite nulos
    df['customer_id'] = df['customer_id'].astype('Int64')

    print("\nTipos despues de la conversion:")
    print(df.dtypes)
    return df

df_orders = correct_types(df_orders)

# PREGUNTA 1: Top 5 clientes por gasto total
ventas_cliente = df_orders.groupby('customer_id').agg({
    'total_amount': 'sum',
    'order_id': 'count'
})
ventas_cliente = ventas_cliente.rename(columns={
    'total_amount': 'total_gastado',
    'order_id': 'cantidad_ordenes'
})
ventas_cliente = ventas_cliente.sort_values(
    'total_gastado',
    ascending=False
)
print("\nTop 5 clientes por gasto:")
print(ventas_cliente.head(5))


# PREGUNTA 2: Producto más vendido por cantidad
productos_vendidos = df_order_items.dropna(
    subset=['product_id', 'quantity']
).groupby('product_id')['quantity'].sum()
productos_vendidos = productos_vendidos.sort_values(
    ascending=False
)
print("\nTop 5 productos por unidades vendidas:")
print(productos_vendidos.head(5))
print(
    f"\nProducto mas vendido: ID {productos_vendidos.idxmax()} "
    f"({productos_vendidos.max()} unidades)"
)

# PREGUNTA 3: Evolución mensual de ventas
df_orders['mes'] = df_orders['order_date'].dt.to_period('M')
ventas_mes = df_orders.groupby('mes')['total_amount'].sum().reset_index()
ventas_mes.columns = ['mes', 'total_ventas']
print("\nVentas por mes:")
print(ventas_mes)


# LOAD: Guardar resultados en CSV
# Crear carpeta output si no existe
os.makedirs('output', exist_ok=True)

# Guardar métricas de negocio
ventas_cliente.to_csv('output/ventas_por_cliente.csv', index=True)
ventas_mes.to_csv('output/ventas_por_mes.csv', index=False)

# Guardar órdenes limpias
df_orders.to_csv('output/orders_clean.csv', index=False)
print("\nArchivos CSV guardados en output/")


# LOAD: Guardar datos en Parquet
df_orders.to_parquet('output/orders_clean.parquet', index=False)
print("Archivo Parquet guardado en output/")

# Comparar tamaños de CSV y Parquet

csv_size = os.path.getsize('output/orders_clean.csv') / 1024
parquet_size = os.path.getsize('output/orders_clean.parquet') / 1024

print(f"Tamaño CSV: {csv_size:.1f} KB")
print(f"Tamaño Parquet: {parquet_size:.1f} KB")

if parquet_size > 0:
    print(f"Relacion de tamaños: {csv_size / parquet_size:.1f}x")