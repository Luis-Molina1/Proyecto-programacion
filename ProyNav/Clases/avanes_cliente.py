import socket


def establecer_conexion_tcp(host):
    puerto = 80
    
    try:
        # SOCK_STREAM indica que usamos el protocolo TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.settimeout(10)
        
        print(f"Conectando a {host} en el puerto {puerto}...")
        sock.connect((host, puerto))
        
        print("Conexión TCP establecida con éxito.")
        return sock

    except socket.timeout:
        print("Error: La conexión excedió el tiempo de espera (Timeout).")
        return None
    except Exception as e:
        print(f"Error al intentar establecer la conexión TCP: {e}")
        return None

mi_socket = establecer_conexion_tcp("www.google.com")