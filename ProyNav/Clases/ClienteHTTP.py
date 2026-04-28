
import http.client
import re
import threading
class ClienteHTTP:
    def funcion_lenta(self):
        import time
        time.sleep(5)
        print("Completado")

    def coneccion(self, url):
        # expresion regular para la URL
        match = re.search(r"(https?)://([^/]+)", url)
        if not match:
            print("URL inválida")
            return
        protocol, host = match.groups()
        
        port = 443 if protocol == 'https' else 80
        print(f"Conectando a {host} en puerto {port}...")
        if protocol == 'https':
            conn = http.client.HTTPSConnection(host, port, timeout=10)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=10)
        try:
            conn.request("GET", "/")
            response = conn.getresponse()
            hilo = threading.Thread(target=self.funcion_lenta)
            hilo.start()
            hilo.join(timeout=3)
            
            print(f"Status: {response.status} {response.reason}")
            print(response.read().decode('utf-8', 'replace')[:300] + "...")
        except Exception as e:
            if 'hilo' in locals() and hilo.is_alive():
                print("Tiempo excedido, la función sigue ejecutándose.")
            print(f"Error: {e}")
        finally:
            conn.close()
            
