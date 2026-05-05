
import http.client
import re
import time

class ClienteHTTP:
    def coneccion(self, url, segundos_retraso=3):
        match = re.search(r"(https?)://([^/]+)(.*)", url)
        if not match:
            print("URL inválida")
            return
        protocol, dominio, ruta = match.groups()
        
        if not ruta:
            ruta = "/"
            
        if protocol == "https":
            port = 443
            conn = http.client.HTTPSConnection(dominio, port, timeout=10)
        else:
            port = 80
            conn = http.client.HTTPConnection(dominio, port, timeout=10)
            
        print(f"Conectando a {dominio} en puerto {port} con ruta {ruta}...")
        
        if segundos_retraso > 0:
            print(f"Esperando {segundos_retraso} segundos...")
            time.sleep(segundos_retraso)
            
        try:
            conn.request("GET", ruta)
            respuesta = conn.getresponse()
            
            print(f"Status: {respuesta.status} {respuesta.reason}")
            print(respuesta.read().decode('utf-8', 'replace') )
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
"""if __name__ == "__main__":
    cliente = ClienteHTTP()
    
    cliente.coneccion("https://icc.utalca.cl")
    
    print("\nPrueba terminada.")
"""