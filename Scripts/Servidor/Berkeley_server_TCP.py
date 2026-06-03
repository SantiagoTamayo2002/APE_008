import socket
import time

# Lista de IPs de los esclavos (PC2 a PC5)
ESCLAVOS = ['192.168.2.11', '192.168.2.12', '192.168.2.13', '192.168.2.14']
PORT = 6001

def ejecutar_berkeley_tcp():
    tiempos_nodos = {}
    delays_nodos = {}
    
    # 1. Obtener la hora del propio coordinador
    t_coordinador = time.time()
    tiempos_nodos['192.168.2.10'] = t_coordinador
    delays_nodos['192.168.2.10'] = 0.0
    
    print(f"Hora del Coordinador (PC1): {t_coordinador}")

    # 2. Solicitar la hora a cada esclavo
    for ip in ESCLAVOS:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(2.0)
            t1 = time.time()
            cliente.connect((ip, PORT))
            
            cliente.sendall(b"DAR_HORA")
            t_esclavo = float(cliente.recv(1024).decode('utf-8'))
            t3 = time.time()
            
            # Estimar delay de red usando RTT/2
            rtt = t3 - t1
            delay = rtt / 2
            
            # Hora estimada del esclavo considerando el viaje
            tiempos_nodos[ip] = t_esclavo + delay
            delays_nodos[ip] = delay
            print(f"Hora recibida de {ip}: {t_esclavo} (Estimada con delay: {tiempos_nodos[ip]})")
            cliente.close()
        except Exception as e:
            print(f"No se pudo conectar con {ip}: {e}")

    if len(tiempos_nodos) <= 1:
        print("Error: No hay suficientes nodos conectados para promediar.")
        return

    # 3. Calcular el promedio de todos los relojes válidos
    promedio_tiempo = sum(tiempos_nodos.values()) / len(tiempos_nodos)
    print(f"\n---> Promedio calculado del sistema: {promedio_tiempo}")

    # 4. Enviar los offsets personalizados a cada uno
    # Para el coordinador mismo:
    offset_coordinador = promedio_tiempo - t_coordinador
    print(f"PC1 (Auto-Ajuste) -> Ajustar por {offset_coordinador:.6f} segundos.")
    
    # Para los esclavos:
    for ip in ESCLAVOS:
        if ip in tiempos_nodos:
            try:
                # El offset es la diferencia entre el promedio y el tiempo actual del esclavo
                offset = promedio_tiempo - tiempos_nodos[ip]
                
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cliente.connect((ip, PORT))
                # Enviamos la instrucción de ajuste
                mensaje = f"AJUSTAR:{offset}"
                cliente.sendall(mensaje.encode('utf-8'))
                print(f"Enviado offset a {ip}: {offset:.6f} seg.")
                cliente.close()
            except Exception as e:
                print(f"Error al enviar ajuste a {ip}: {e}")
                
    # Guardar en log txt local
    with open("registro_berkeley_tcp.txt", "a") as f:
        f.write(f"--- Ejecución Berkeley TCP ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
        for node_ip, node_time in tiempos_nodos.items():
            f.write(f"Nodo {node_ip} -> Tiempo estimado: {node_time}\n")
        f.write(f"Promedio global del sistema: {promedio_tiempo}\n\n")

if __name__ == "__main__":
    ejecutar_berkeley_tcp()