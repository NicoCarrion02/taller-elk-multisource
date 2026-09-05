import os
from typing import Dict, Any

# PostgreSQL Configuration
POSTGRES_CONFIG: Dict[str, Any] = {
  "host": os.getenv("POSTGRES_HOST", "localhost"),
  "port": int(os.getenv("POSTGRES_PORT", 5432)),
  "user": os.getenv("POSTGRES_USER", "usuario_taller"),
  "password": os.getenv("POSTGRES_PASSWORD", "password_taller"),
  "database": os.getenv("POSTGRES_DB", "bd_taller"),
}

# MySQL Configuration
MYSQL_CONFIG: Dict[str, Any] = {
  "host": os.getenv("MYSQL_HOST", "localhost"),
  "port": int(os.getenv("MYSQL_PORT", 3306)),
  "user": os.getenv("MYSQL_USER", "usuario_taller"),
  "password": os.getenv("MYSQL_PASSWORD", "password_taller"),
  "database": os.getenv("MYSQL_DB", "bd_taller"),
}

# Aliases for convenience
postgres_config = POSTGRES_CONFIG
mysql_config = MYSQL_CONFIG


def get_postgres_url(config: Dict[str, Any] = None) -> str:
  """
  Generate an SQLAlchemy connection URL string for PostgreSQL.
  """
  cfg = config or POSTGRES_CONFIG
  return f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"


def get_mysql_url(config: Dict[str, Any] = None) -> str:
  """
  Generate an SQLAlchemy connection URL string for MySQL.
  """
  cfg = config or MYSQL_CONFIG
  return f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"