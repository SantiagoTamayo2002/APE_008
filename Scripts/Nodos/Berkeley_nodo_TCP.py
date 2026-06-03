import socket
import time

HOST = '0.0.0.0'  # Escucha en todas sus interfaces de red
PORT = 6001

def iniciar_esclavo_tcp():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Esclavo TCP listo y esperando al coordinador en el puerto {PORT}...")

    while True:
        conn, addr = server.accept()
        try:
            data = conn.recv(1024).decode('utf-8')
            
            if data == "DAR_HORA":
                # Enviamos nuestra hora local actual de inmediato
                hora_local = time.time()
                conn.sendall(str(hora_local).encode('utf-8'))
                
            elif data.startswith("AJUSTAR:"):
                offset = float(data.split(":")[1])
                print(f"\n[ORDEN RECIBIDA] Ajustar reloj sumando: {offset:.6f} segundos.")
                
                # NOTA: En un entorno de producción aquí se alteraría el reloj del OS. 
                # Para la práctica calculamos cómo quedaría el nuevo tiempo simulado.
                nuevo_tiempo = time.time() + offset
                print(f"Sincronizado. Tiempo anterior: {time.time()} -> Nuevo Tiempo: {nuevo_tiempo}")
                
        except Exception as e:
            print(f"Error procesando petición: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    iniciar_esclavo_tcp()