
import http.client
import re
import time

class ClienteHTTP:
    def coneccion(self, url, segundos_retraso=3):
        match = re.search(r"(https?)://([^/]+)", url)
        if not match:
            print("URL inválida")
            return
        protocol, dominio = match.groups()
        
        port = 80
        print(f"Conectando a {dominio} en puerto {port}...")
        
        if segundos_retraso > 0:
            print(f"Esperando {segundos_retraso} segundos...")
            time.sleep(segundos_retraso)
            
        conn = http.client.HTTPConnection(dominio, port, timeout=10)
            
        try:
            conn.request("GET", "/")
            respuesta = conn.getresponse()
            
            print(f"Status: {respuesta.status} {respuesta.reason}")
            print(respuesta.read().decode('utf-8', 'replace')[:300] + "...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
if __name__ == "__main__":
    cliente = ClienteHTTP()
    
    cliente.coneccion("http://utalca.cl")
    
    print("\nPrueba terminada.")
