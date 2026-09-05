from download_data import download_data
from split_data import split_file
import os
import json

def engine():
  path = "data/raw/olist_order_reviews_dataset"
  download_data("olistbr/brazilian-ecommerce", path)
