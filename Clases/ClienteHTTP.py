import http.client
import time
import urllib.parse
import ssl

class ClienteHTTP:
    def obtener_contenido(self, url, segundos_retraso=3, redirecciones=5):
        if redirecciones == 0:
            print("Error: Demasiadas redirecciones")
            return None

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
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(dominio, port, timeout=10, context=context)
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

            # redirecciones
            if respuesta.status in (301, 302, 303, 307, 308):
                nueva_url = respuesta.getheader('Location')
                if nueva_url:
                    nueva_url = urllib.parse.urljoin(url, nueva_url)
                    print(f"Redirigiendo a: {nueva_url}")
                    return self.obtener_contenido(nueva_url, segundos_retraso, redirecciones - 1)

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