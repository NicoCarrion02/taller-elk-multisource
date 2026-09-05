import os
import sys
from typing import List, Optional, Dict, Any, Union
import pandas as pd
from sqlalchemy import create_engine, Engine

# Allow importing config from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import (
  POSTGRES_CONFIG,
  MYSQL_CONFIG,
  get_postgres_url,
  get_mysql_url,
)

def get_engine(
  db_type: str = "postgres",
  config: Optional[Dict[str, Any]] = None,
  **engine_kwargs
) -> Engine:
    """
    Create and return a SQLAlchemy Engine for PostgreSQL or MySQL.

    Args:
        db_type (str): "postgres" or "mysql".
        config (dict, optional): Custom connection dictionary. Defaults to config in settings.py.
        **engine_kwargs: Additional arguments passed to sqlalchemy.create_engine.

    Returns:
        Engine: SQLAlchemy database engine.
    """
    db_type = db_type.lower()
    if db_type in ("postgres", "postgresql"):
      url = get_postgres_url(config)
    elif db_type in ("mysql", "mariadb"):
      url = get_mysql_url(config)
    else:
        raise ValueError(f"Unsupported database type: '{db_type}'. Must be 'postgres' or 'mysql'.")

    return create_engine(url, **engine_kwargs)

def dataframe_to_db(
    df: pd.DataFrame,
    table_name: str,
    con: Optional[Union[Engine, str]] = None,
    db_type: str = "postgres",
    db_config: Optional[Dict[str, Any]] = None,
    if_exists: str = "replace",
    index: bool = False,
    chunksize: Optional[int] = 1000,
    **to_sql_kwargs
) -> None:
  """
  Pass a pandas DataFrame into a database table.
  Creates the table automatically if it does not already exist.

  Args:
      df (pd.DataFrame): DataFrame to insert.
      table_name (str): Name of the target table.
      con (Engine or str, optional): SQLAlchemy engine or connection URL. If None, created from db_type & db_config.
      db_type (str): "postgres" or "mysql" (used if con is not provided). Defaults to "postgres".
      db_config (dict, optional): Database configuration dictionary if con is None.
      if_exists (str): How to behave if the table already exists ('fail', 'replace', 'append'). Defaults to 'replace'.
      index (bool): Whether to write the DataFrame index as a column. Defaults to False.
      chunksize (int, optional): Number of rows to insert per batch. Defaults to 1000.
      **to_sql_kwargs: Extra keyword arguments forwarded to `df.to_sql`.
  """
  con = get_engine(db_type=db_type, config=db_config)

  print(f"Loading {len(df)} rows into table '{table_name}' (mode: {if_exists})...")
  df.to_sql(
    name=table_name,
    con=con,
    if_exists=if_exists,
    index=index,
    chunksize=chunksize,
    **to_sql_kwargs
  )
  print(f"Successfully loaded data into table '{table_name}'.")


def load_csv_to_db(
  file_path: str,
  table_name: Optional[str] = None,
  db_type: str = "postgres",
  db_config: Optional[Dict[str, Any]] = None,
  if_exists: str = "replace",
  chunksize: Optional[int] = 1000,
  **read_csv_kwargs
) -> None:
  """
  Read a CSV file and load its content into a database table.

  Args:
      file_path (str): Path to CSV file.
      table_name (str, optional): Target table name. Defaults to the CSV filename without extension.
      db_type (str): "postgres" or "mysql".
      db_config (dict, optional): Custom DB config.
      if_exists (str): 'fail', 'replace', or 'append'.
      chunksize (int, optional): Batch insert size.
      **read_csv_kwargs: Extra arguments for `pd.read_csv`.
  """
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

  if table_name is None:
    table_name = os.path.splitext(os.path.basename(file_path))[0]

  df = pd.read_csv(file_path, **read_csv_kwargs)
  dataframe_to_db(
      df=df,
      table_name=table_name,
      db_type=db_type,
      db_config=db_config,
      if_exists=if_exists,
      chunksize=chunksize
  )

def ingest_data(file_names: list[str], db_type: str):
  if db_type not in ['postgres', 'mysql']:
    raise ValueError('db_type must be postgres or mysql')
  
  if len(file_names) == 0:
    raise ValueError('file_names must have values')

  config = MYSQL_CONFIG
  if (db_type == 'postgres'):
    config = POSTGRES_CONFIG

  root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  for f in file_names:
    file_path = os.path.join(root_dir, 'data', 'raw', 'olist_order_reviews_dataset', f)
    table_name = f.split('.')[0]
    load_csv_to_db(file_path, table_name, db_type, config, 'replace')
    
