CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(100),
    customer_state VARCHAR(2)
);

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(100),
    seller_state VARCHAR(2)
);

-- Cargar datos desde los CSVs mapeados
COPY customers FROM '/data/olist_customers_dataset.csv' DELIMITER ',' CSV HEADER;
COPY sellers FROM '/data/olist_sellers_dataset.csv' DELIMITER ',' CSV HEADER;