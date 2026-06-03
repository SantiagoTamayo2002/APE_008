import socket
import threading
import time
import json

MI_ID = 1  # 1 para PC1, 2 para PC2, etc. (Índice en el vector será MI_ID - 1)
IPS_RED = {1: '192.168.2.10', 2: '192.168.2.11', 3: '192.168.2.12', 4: '192.168.2.13', 5: '192.168.2.14'}
PUERTO = 8001

# Inicializar vector de 5 posiciones [0, 0, 0, 0, 0]
vector_tiempo = [0, 0, 0, 0, 0]
lock = threading.Lock()

def hilo_receptor_vector():
    global vector_tiempo
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PUERTO))
    
    while True:
        data, addr = sock.recvfrom(1024)
        payload = json.loads(data.decode('utf-8'))
        
        v_recibido = payload['vector']
        emisor = payload['emisor']
        texto = payload['texto']
        
        with lock:
            # Regla de recepción vectorial:
            # 1. W[i] = max(W[i], V[i]) para todas las posiciones
            for i in range(5):
                vector_tiempo[i] = max(vector_tiempo[i], v_recibido[i])
            # 2. Incrementar mi propia posición
            vector_tiempo[MI_ID - 1] += 1
            
            print(f"\n[RECIBIDO] Mensaje: '{texto}' de PC{emisor}")
            print(f"Vector del mensaje: {v_recibido}")
            print(f"Mi Vector Actualizado: {vector_tiempo}")

def enviar_mensaje_vector(destino_id, texto):
    global vector_tiempo
    if destino_id not in IPS_RED or destino_id == MI_ID:
        return
    
    with lock:
        # Regla de envío: incrementar mi propia posición antes de mandar copia
        vector_tiempo[MI_ID - 1] += 1
        payload = {
            'emisor': MI_ID,
            'vector': list(vector_tiempo), # Clonar lista
            'texto': texto
        }
        print(f"\n[ENVÍO] Enviando a PC{destino_id}. Vector copiado: {payload['vector']}")
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(payload).encode('utf-8'), (IPS_RED[destino_id], PUERTO))
    sock.close()

if __name__ == "__main__":
    threading.Thread(target=hilo_receptor_vector, daemon=True).start()
    time.sleep(2)
    
    # Simulación guiada de la Guía de laboratorio:
    # PC2 envía a PC3. Mientras viaja, PC1 envía a PC3. PC3 recibe ambos de forma concurrente.
    if MI_ID == 2:
        input("Presione ENTER para simular envío de PC2 a PC3...")
        enviar_mensaje_vector(3, "Mensaje desde PC2")
    elif MI_ID == 1:
        input("Presione ENTER para simular envío concurrente de PC1 a PC3...")
        enviar_mensaje_vector(3, "Mensaje desde PC1")
    else:
        print("Esperando eventos en la red...")

    while True:
        time.sleep(1)