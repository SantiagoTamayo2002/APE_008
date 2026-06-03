import socket
import threading
import time
import json

MI_ID = 1  
IPS_RED = {1: '192.168.2.10', 2: '192.168.2.11', 3: '192.168.2.12', 4: '192.168.2.13', 5: '192.168.2.14'}
PUERTO = 8002

vector_tiempo = [0, 0, 0, 0, 0]
lock = threading.Lock()

def manejar_cliente_vector(conn):
    global vector_tiempo
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            payload = json.loads(data)
            v_recibido = payload['vector']
            with lock:
                for i in range(5):
                    vector_tiempo[i] = max(vector_tiempo[i], v_recibido[i])
                vector_tiempo[MI_ID - 1] += 1
                print(f"\n[TCP RECIBIDO] De PC{payload['emisor']}: '{payload['texto']}'")
                print(f"Vector Resultante: {vector_tiempo}")
    except: pass
    finally: conn.close()

def servidor_vector_tcp():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', PUERTO))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=manejar_cliente_vector, args=(conn,), daemon=True).start()

def enviar_vector_tcp(destino_id, texto):
    global vector_tiempo
    with lock:
        vector_tiempo[MI_ID - 1] += 1
        payload = {'emisor': MI_ID, 'vector': list(vector_tiempo), 'texto': texto}
        print(f"\n[TCP ENVÍO] Enviando a PC{destino_id}. Vector: {payload['vector']}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((IPS_RED[destino_id], PUERTO))
        s.sendall(json.dumps(payload).encode('utf-8'))
        s.close()
    except Exception as e:
        print(f"Error de conexión con PC{destino_id}: {e}")

if __name__ == "__main__":
    threading.Thread(target=servidor_vector_tcp, daemon=True).start()
    time.sleep(2)
    
    # Ejecución interactiva
    while True:
        cmd = input("\nEscribe el ID destino (1-5) para enviar mensaje TCP o 'salir': ")
        if cmd == 'salir': break
        if cmd.isdigit() and int(cmd) in IPS_RED:
            enviar_vector_tcp(int(cmd), f"Test Vector TCP desde PC{MI_ID}")