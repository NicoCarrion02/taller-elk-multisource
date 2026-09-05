from download_data import download_data
from split_data import split_file
import os
import json

def engine():
  path = download_data("olistbr/brazilian-ecommerce", "data/raw/olist_order_reviews_dataset")
  