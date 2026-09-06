import pandas as pd
import json
import time
import os

print("Cargando y procesando red espacial de Olist...")

# Cargar datasets
orders = pd.read_csv('./data/olist_orders_dataset.csv')
customers = pd.read_csv('./data/olist_customers_dataset.csv')
geo = pd.read_csv('./data/olist_geolocation_dataset.csv')

# Filtrar red por centroides para evitar duplicados de coordenadas por código postal
geo_centroids = geo.groupby('geolocation_zip_code_prefix').agg({
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean'
}).reset_index()

# Unir pedidos con clientes y luego con coordenadas
df_merged = orders.merge(customers, on='customer_id', how='inner')
df_merged = df_merged.merge(
    geo_centroids, 
    left_on='customer_zip_code_prefix', 
    right_on='geolocation_zip_code_prefix', 
    how='inner'
)

# Seleccionar pedidos aprobados o entregados
df_filtered = df_merged[df_merged['order_status'].isin(['delivered', 'shipped', 'approved'])].copy()

# Ordenar cronológicamente para simular el flujo histórico como si fuera actual
df_filtered.sort_values('order_purchase_timestamp', inplace=True)

archivo_salida = './data/telemetria_pedidos.json'
if os.path.exists(archivo_salida):
    os.remove(archivo_salida)

print("Iniciando emisión de eventos en tiempo real...")

with open(archivo_salida, 'a') as f:
    for _, row in df_filtered.iterrows():
        # Construir el objeto JSON con tipificación geo_point para Elastic
        evento = {
            "order_id": row['order_id'],
            "customer_id": row['customer_id'],
            "status": row['order_status'],
            "city": row['customer_city'],
            "timestamp": pd.Timestamp.now().isoformat(), # Reemplazar con hora actual para simulación
            "location": {
                "lat": row['geolocation_lat'],
                "lon": row['geolocation_lng']
            }
        }
        
        # Escribir línea (NDJSON)
        f.write(json.dumps(evento) + '\n')
        f.flush()
        
        time.sleep(1.5) # Simular latencia de red de 1.5 segundos