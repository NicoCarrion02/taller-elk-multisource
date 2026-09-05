from download_data import download_data, copy_data_to_dst
from pass_to_db import ingest_data
import os
import json

def engine():
  print('Downloading files. If this fails, check your credentials')
  path = "data/raw/olist_order_reviews_dataset"
  download_data("olistbr/brazilian-ecommerce", path)
  #postgres = ['olist_customers_dataset.csv', 'olist_geolocation_dataset.csv']
  #mysql = ['olist_order_items_dataset.csv', 'olist_order_payments_dataset.csv', 'olist_order_reviews_dataset.csv', 'olist_orders_dataset.csv']
  
  #ingest_data(postgres, 'postgres')
  #ingest_data(mysql, 'mysql')

  print('Copying files')
  files = [
    "olist_products_dataset.csv",               # Fuente 1: Batch (Catálogo)
    "product_category_name_translation.csv",    # Fuente 1: Batch (Traducciones)
    "olist_customers_dataset.csv",              # Fuente 2: Batch (SQL Clientes)
    "olist_sellers_dataset.csv",                # Fuente 2: Batch (SQL Vendedores)
    "olist_order_reviews_dataset.csv",          # Fuente 3: NRT (Logs de reseñas)
    "olist_orders_dataset.csv",                 # Fuente 4: NRT (Telemetría Python)
    "olist_geolocation_dataset.csv"             # Fuente 4: NRT (Telemetría Python)
  ]

  root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  copy_data_to_dst(os.path.join(root_dir, path), os.path.join(root_dir, 'data', 'processed'), files) 

  print('Everything that could fail, did not fail. c:')


if __name__ == "__main__":
  engine()