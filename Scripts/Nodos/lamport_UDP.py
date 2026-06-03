import socket
import threading
import time
import json

# --- CONFIGURACIÓN DE RED (Cambiar según cada PC) ---
MI_ID = 1  # PC1=1, PC2=2, PC3=3, PC4=4, PC5=5
IPS_RED = {
    1: '192.168.2.10',
    2: '192.168.2.11',
    3: '192.168.2.12',
    4: '192.168.2.13',
    5: '192.168.2.14'
}
PUERTO = 7001

# --- VARIABLES DEL ALGORITMO ---
reloj_lamport = 0
lock = threading.Lock()

def hilo_receptor():
    global reloj_lamport
    sock_recibe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_recibe.bind(('0.0.0.0', PUERTO))
    print(f"[RECEPTOR] Escuchando en el puerto {PUERTO}...")
    
    while True:
        data, addr = sock_recibe.recvfrom(1024)
        payload = json.loads(data.decode('utf-8'))
        
        contador_recibido = payload['contador']
        texto = payload['texto']
        emisor = payload['emisor']
        
        with lock:
            # Regla de recepción de Lamport
            reloj_lamport = max(reloj_lamport, contador_recibido) + 1
            print(f"\n[MENSAJE] De PC{emisor}: '{texto}' (Reloj Recibido: {contador_recibido})")
            print(f"[RELOJ ACTUALIZADO] Mi nuevo reloj es: {reloj_lamport}")

def enviar_mensaje(destino_id, texto):
    global reloj_lamport
    if destino_id not in IPS_RED or destino_id == MI_ID:
        return
    
    with lock:
        # Regla de envío de Lamport
        reloj_lamport += 1
        payload = {
            'emisor': MI_ID,
            'contador': reloj_lamport,
            'texto': texto
        }
        print(f"\n[ENVÍO] Enviando a PC{destino_id} con Reloj={reloj_lamport}")
    
    sock_envio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_envio.sendto(json.dumps(payload).encode('utf-8'), (IPS_RED[destino_id], PUERTO))
    sock_envio.close()

if __name__ == "__main__":
    # Iniciar receptor en background
    t = threading.Thread(target=hilo_receptor, daemon=True)
    t.start()
    
    time.sleep(2) # Esperar a que todos levanten el socket
    
    print("\n--- Modo Simulación Activado ---")
    print("Ingresa el ID del destino (1-5) y el texto, o presiona ENTER para la prueba automática de 3 mensajes.")
    entrada = input("Presiona ENTER para iniciar ráfaga automática o escribe 'manual': ")
    
    if entrada != 'manual':
        # Dinámica guiada: Enviar 3 mensajes a destinos aleatorios/distintos
        destinos_ejemplo = [id_node for id_node in IPS_RED.keys() if id_node != MI_ID][:3]
        for idx, dest in enumerate(destinos_ejemplo):
            time.sleep(idx * 1.5) # Espaciar un poco los envíos concurrentes
            enviar_mensaje(dest, f"Mensaje automático {idx+1} desde PC{MI_ID}")
    
    # Mantener el script vivo para seguir recibiendo mensajes de los demás
    while True:
        time.sleep(1)