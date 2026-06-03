import socket
import time
import datetime

SERVER_HOST = '192.168.2.10'
SERVER_PORT = 5001

def sincronizar_cliente():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    
    # t1: Hora local justo antes de enviar
    t1 = time.time()
    client.sendall(b"REQUEST_TIME")
    
    # Recibir t2 del servidor
    data = client.recv(1024).decode('utf-8')
    # t3: Hora local justo al recibir
    t3 = time.time()
    
    t2 = float(data)
    
    # Cálculos del Algoritmo de Cristian
    rtt = t3 - t1
    delay = rtt / 2
    nuevo_tiempo = t2 + delay
    
    # Diferencia entre la nueva hora calculada y la del servidor (t2)
    # Nota: Idealmente esta diferencia debería tender a cero o al delay real.
    diferencia = nuevo_tiempo - t2
    
    print(f"--- Resultados Sincronización ---")
    print(f"t1 (Envío): {datetime.datetime.fromtimestamp(t1)}")
    print(f"t2 (Servidor): {datetime.datetime.fromtimestamp(t2)}")
    print(f"t3 (Recepción): {datetime.datetime.fromtimestamp(t3)}")
    print(f"RTT: {rtt:.6f} seg | Delay: {delay:.6f} seg")
    print(f"Nuevo Tiempo Calculado: {datetime.datetime.fromtimestamp(nuevo_tiempo)}")
    
    # Enviar reporte de vuelta al coordinador para el archivo .txt
    reporte = f"RTT={rtt:.6f}s, Delay={delay:.6f}s, Dif_con_Servidor={diferencia:.6f}s"
    client.sendall(reporte.encode('utf-8'))
    
    client.close()

if __name__ == "__main__":
    sincronizar_cliente()