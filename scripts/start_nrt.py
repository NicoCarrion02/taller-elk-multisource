import subprocess
import sys

print("Iniciando todos los flujos NRT en paralelo...")

# Iniciar ambos scripts en segundo plano
p1 = subprocess.Popen([sys.executable, "scripts/stream_reviews.py"])
p2 = subprocess.Popen([sys.executable, "scripts/stream_spatial_orders.py"])

try:
    # Mantener el script orquestador en ejecución
    p1.wait()
    p2.wait()
except KeyboardInterrupt:
    print("\nDeteniendo flujos NRT...")
    p1.terminate()
    p2.terminate()