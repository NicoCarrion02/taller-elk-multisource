import kagglehub

def download_data(dataset, path):
  """
  Download a dataset from Kaggle Hub
  
  Args:
    dataset (str): Name of the dataset
    path (str): Path to save the dataset
  """
  root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  print("Root dir:", root_dir)
  path = os.path.join(root_dir, path)
  print("Path:", path)
  os.makedirs(path, exist_ok=True)

  data = kagglehub.dataset_download(dataset, path)
  return data

if __name__ == "__main__":
  path = download_data("olistbr/brazilian-ecommerce", "data/raw/olist_order_reviews_dataset.csv")
  print("Path to dataset files:", path)