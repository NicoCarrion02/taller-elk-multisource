from download_data import download_data
from pass_to_db import ingest_data
import os
import json

def engine():
  path = "data/raw/olist_order_reviews_dataset"
  download_data("olistbr/brazilian-ecommerce", path)
  postgres = ['olist_customers_dataset.csv', 'olist_geolocation_dataset.csv']
  mysql = ['olist_order_items_dataset.csv', 'olist_order_payments_dataset.csv', 'olist_order_reviews_dataset.csv', 'olist_orders_dataset.csv']
  
  ingest_data(postgres, 'postgres')
  ingest_data(mysql, 'mysql')
  
