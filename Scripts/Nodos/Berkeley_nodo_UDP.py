import socket
import time

HOST = '0.0.0.0'
PORT = 6002

def iniciar_esclavo_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"Esclavo UDP listo y escuchando en el puerto {PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        mensaje = data.decode('utf-8')
        
        if mensaje == "DAR_HORA":
            hora_local = time.time()
            sock.sendto(str(hora_local).encode('utf-8'), addr)
            
        elif mensaje.startswith("AJUSTAR:"):
            offset = float(mensaje.split(":")[1])
            print(f"\n[ORDEN UDP RECIBIDA] Ajustar reloj sumando: {offset:.6f} segundos.")
            nuevo_tiempo = time.time() + offset
            print(f"Sincronizado (UDP). Tiempo anterior: {time.time()} -> Nuevo Tiempo: {nuevo_tiempo}")

if __name__ == "__main__":
    iniciar_esclavo_udp()