#!/bin/bash
echo "Iniciando stream de reviews..."
touch ./data/reviews.log

# Leer desde la línea 2 para saltar los encabezados
tail -n +2 ./data/olist_order_reviews_dataset.csv | while IFS= read -r line; do
  echo "$line" >> ./data/reviews.log
  # Pausa de 1 segundo entre cada escritura para simular tráfico en vivo
  sleep 1 
done