import socket
import time
import datetime

SERVER_HOST = '192.168.2.10'
SERVER_PORT = 5002

def sincronizar_cliente_udp():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2.0) # Timeout por si se pierde el paquete
    
    # t1: Registro de salida
    t1 = time.time()
    client.sendto(b"REQUEST_TIME", (SERVER_HOST, SERVER_PORT))
    
    try:
        data, addr = client.recvfrom(1024)
        # t3: Registro de entrada
        t3 = time.time()
        
        t2 = float(data.decode('utf-8'))
        
        # Fórmulas de Cristian
        rtt = t3 - t1
        delay = rtt / 2
        nuevo_tiempo = t2 + delay
        diferencia = nuevo_tiempo - t2
        
        print(f"--- Resultados UDP ---")
        print(f"RTT: {rtt:.6f} seg | Delay: {delay:.6f} seg")
        print(f"Hora Ajustada: {datetime.datetime.fromtimestamp(nuevo_tiempo)}")
        
        # Enviar reporte al servidor
        reporte = f"REPORTE:RTT={rtt:.6f}s, Delay={delay:.6f}s, Dif_con_Servidor={diferencia:.6f}s"
        client.sendto(reporte.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        
    except socket.timeout:
        print("Error: Tiempo de espera agotado (Paquete perdido).")
    finally:
        client.close()

if __name__ == "__main__":
    sincronizar_cliente_udp()