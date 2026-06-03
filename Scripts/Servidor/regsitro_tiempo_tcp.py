import socket
import time
import threading

HOST = '192.168.2.10'
PORT = 5001

def manejar_cliente(conn, addr):
    try:
        # t2: Hora del servidor justo al recibir la petición
        t2 = time.time()
        # Enviamos t2 inmediatamente al cliente
        conn.sendall(str(t2).encode('utf-8'))
        
        # Esperamos a que el cliente nos mande su reporte para el registro
        reporte = conn.recv(1024).decode('utf-8')
        if reporte:
            log_msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] Desde {addr[0]}: {reporte}\n"
            print(log_msg.strip())
            with open("registro_tiempo_tcp.txt", "a") as f:
                f.write(log_msg)
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor TCP (PC1) escuchando en {HOST}:{PORT}...")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()