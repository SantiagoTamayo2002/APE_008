import socket
import threading
import time
import json

MI_ID = 1  
IPS_RED = {1: '192.168.2.10', 2: '192.168.2.11', 3: '192.168.2.12', 4: '192.168.2.13', 5: '192.168.2.14'}
PUERTO = 7002

reloj_lamport = 0
lock = threading.Lock()

def manejar_conexion_tcp(conn, addr):
    global reloj_lamport
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            payload = json.loads(data)
            contador_recibido = payload['contador']
            with lock:
                reloj_lamport = max(reloj_lamport, contador_recibido) + 1
                print(f"\n[TCP] Recibido de PC{payload['emisor']}: '{payload['texto']}' (Reloj: {contador_recibido})")
                print(f"[RELOJ] Nuevo valor local: {reloj_lamport}")
    except Exception as e:
        pass
    finally:
        conn.close()

def servidor_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', PUERTO))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=manejar_conexion_tcp, args=(conn, addr), daemon=True).start()

def enviar_tcp(destino_id, texto):
    global reloj_lamport
    with lock:
        reloj_lamport += 1
        payload = {'emisor': MI_ID, 'contador': reloj_lamport, 'texto': texto}
        print(f"\n[TCP ENVÍO] A PC{destino_id} con Reloj={reloj_lamport}")
        
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((IPS_RED[destino_id], PUERTO))
        s.sendall(json.dumps(payload).encode('utf-8'))
        s.close()
    except Exception as e:
        print(f"Error enviando TCP a PC{destino_id}: {e}")

if __name__ == "__main__":
    threading.Thread(target=servidor_tcp, daemon=True).start()
    time.sleep(2)
    
    destinos = [id_node for id_node in IPS_RED.keys() if id_node != MI_ID][:3]
    for idx, dest in enumerate(destinos):
        time.sleep(1)
        enviar_tcp(dest, f"Hola PC{dest}, soy PC{MI_ID} por TCP")
        
    while True: time.sleep(1)