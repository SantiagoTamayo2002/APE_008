import socket
import time

ESCLAVOS = ['192.168.2.11', '192.168.2.12', '192.168.2.13', '192.168.2.14']
PORT_ESCLAVO = 6002

def ejecutar_berkeley_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.5) # Timeout corto para saltar si un nodo está apagado
    
    tiempos_nodos = {}
    
    t_coordinador = time.time()
    tiempos_nodos['192.168.2.10'] = t_coordinador
    print(f"Hora del Coordinador (PC1): {t_coordinador}")

    # 1. Solicitar hora por UDP
    for ip in ESCLAVOS:
        try:
            t1 = time.time()
            sock.sendto(b"DAR_HORA", (ip, PORT_ESCLAVO))
            
            data, addr = sock.recvfrom(1024)
            t3 = time.time()
            
            t_esclavo = float(data.decode('utf-8'))
            delay = (t3 - t1) / 2
            
            tiempos_nodos[ip] = t_esclavo + delay
            print(f"Hora recibida de {ip}: {t_esclavo} (Con delay: {tiempos_nodos[ip]})")
        except socket.timeout:
            print(f"Timeout: El nodo {ip} no respondió.")
            
    if len(tiempos_nodos) <= 1:
        print("Error: No hay suficientes respuestas.")
        return

    # 2. Calcular promedio
    promedio_tiempo = sum(tiempos_nodos.values()) / len(tiempos_nodos)
    print(f"\n---> Promedio calculado del sistema (UDP): {promedio_tiempo}")

    # 3. Enviar orden de ajuste mediante UDP
    for ip in ESCLAVOS:
        if ip in tiempos_nodos:
            offset = promedio_tiempo - tiempos_nodos[ip]
            mensaje = f"AJUSTAR:{offset}"
            sock.sendto(mensaje.encode('utf-8'), (ip, PORT_ESCLAVO))
            print(f"Offset enviado a {ip}: {offset:.6f} seg.")
            
    print(f"PC1 (Auto-Ajuste) -> Ajustar por {promedio_tiempo - t_coordinador:.6f} segundos.")
    
    # Registro en archivo txt
    with open("registro_berkeley_udp.txt", "a") as f:
        f.write(f"--- Ejecución Berkeley UDP ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
        f.write(f"Promedio global: {promedio_tiempo}\n\n")

if __name__ == "__main__":
    ejecutar_berkeley_udp()