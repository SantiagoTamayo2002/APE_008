import socket
import time

HOST = '192.168.2.10'
PORT = 5002

def iniciar_servidor_udp():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Servidor UDP (PC1) escuchando en {HOST}:{PORT}...")
    
    while True:
        data, addr = server.recvfrom(1024)
        mensaje = data.decode('utf-8')
        
        if mensaje == "REQUEST_TIME":
            # t2: Lo más pronto posible
            t2 = time.time()
            server.sendto(str(t2).encode('utf-8'), addr)
        
        elif mensaje.startswith("REPORTE:"):
            # Registro de los datos en el archivo txt
            reporte = mensaje.replace("REPORTE:", "")
            log_msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] Desde UDP {addr[0]}: {reporte}\n"
            print(log_msg.strip())
            with open("registro_tiempo_udp.txt", "a") as f:
                f.write(log_msg)

if __name__ == "__main__":
    iniciar_servidor_udp()