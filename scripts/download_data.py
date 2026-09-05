import kagglehub
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

print("Iniciando descarga del dataset de Olist...")

# Descargar el dataset específico de Olist desde Kaggle
ruta_cache = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
print("Descarga completada. Filtrando archivos para el taller ELK...")

carpeta_destino = "./data"

archivos_requeridos = [
    "olist_products_dataset.csv",               # Fuente 1: Batch (Catálogo)
    "product_category_name_translation.csv",    # Fuente 1: Batch (Traducciones)
    "olist_customers_dataset.csv",              # Fuente 2: Batch (SQL Clientes)
    "olist_sellers_dataset.csv",                # Fuente 2: Batch (SQL Vendedores)
    "olist_order_reviews_dataset.csv",          # Fuente 3: NRT (Logs de reseñas)
    "olist_orders_dataset.csv",                 # Fuente 4: NRT (Telemetría Python)
    "olist_geolocation_dataset.csv"             # Fuente 4: NRT (Telemetría Python)
]

os.makedirs(carpeta_destino, exist_ok=True)

archivos_copiados = 0
for archivo in os.listdir(ruta_cache):
    if archivo in archivos_requeridos:
        ruta_origen = os.path.join(ruta_cache, archivo)
        ruta_final = os.path.join(carpeta_destino, archivo)
        
        shutil.copy(ruta_origen, ruta_final)
        archivos_copiados += 1
        print(f"✅ Copiado: {archivo}")

print(f"\nSe copiaron {archivos_copiados} archivos a la carpeta '{carpeta_destino}'.")