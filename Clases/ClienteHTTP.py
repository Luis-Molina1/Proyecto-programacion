
import http.client
import time
import urllib.parse

class ClienteHTTP:
    def obtener_contenido(self, url, segundos_retraso=3):
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            print("URL inválida")
            return None

        protocol = parsed.scheme
        dominio = parsed.netloc
        ruta = parsed.path or "/"
        if parsed.query:
            ruta += "?" + parsed.query

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
            contenido = respuesta.read().decode('utf-8', 'replace')
            return respuesta.status, respuesta.reason, contenido
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()
    def coneccion(self, url, segundos_retraso=3):
        resultado = self.obtener_contenido(url, segundos_retraso)
        if resultado is None:
            return None

        status, reason, contenido = resultado
        print(f"Status: {status} {reason}")
        print(contenido)
        return contenido


if __name__ == "__main__":
    cliente = ClienteHTTP()
    
    cliente.coneccion("https://icc.utalca.cl")
    
    print("\nPrueba terminada.")