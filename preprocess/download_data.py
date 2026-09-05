import kagglehub
import os
import shutil

def download_data(dataset, path):
  """
  Download a dataset from Kaggle Hub
  
  Args:
    dataset (str): Name of the dataset
    path (str): Path to save the dataset
  """
  root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  path = os.path.join(root_dir, path)
  if not os.path.exists(path):
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    saved_path = kagglehub.dataset_download(dataset)
    shutil.move(saved_path, path)

def copy_data_to_dst(ori: str, dst: str, files: list[str]):
  os.makedirs(dst, exist_ok=True)
  for f in files:
    shutil.copy(os.path.join(ori, f), os.path.join(dst, f))