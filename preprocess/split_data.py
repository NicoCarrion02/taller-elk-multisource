import pandas as pd
import json

def read_file(path):
  """
  Read a CSV file and return a pandas DataFrame
  
  Args:
    path (str): Path to the CSV file
  """
  df = pd.read_csv(path)
  return df
  

def split_file(path, size):
  """
  Split a CSV file into chunks of a specified size
  
  Args:
    path (str): Path to the CSV file
    size (int): Size of each chunk
  """
  df = pd.read_csv(path)
  for i in range(0, len(df), size):
    yield df[i:i+size]
  