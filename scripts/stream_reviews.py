import time

print("Iniciando stream de reviews...")
csv_file = './data/olist_order_reviews_dataset.csv'
log_file = './data/reviews.log'

# Limpiar o crear el archivo de log vacío
open(log_file, 'w', encoding='utf-8').close()

try:
    with open(csv_file, 'r', encoding='utf-8') as f_in, \
         open(log_file, 'a', encoding='utf-8') as f_out:
        
        next(f_in)  # Saltar los encabezados del CSV
        
        for line in f_in:
            f_out.write(line)
            f_out.flush() # Forzar la escritura a disco para que Logstash lo lea
            time.sleep(1) # Simular 1 segundo de latencia
            
except FileNotFoundError:
    print(f"Error: No se encontró {csv_file}. Ejecuta download_data.py primero.")