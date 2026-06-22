import http.client
import time
import urllib.parse
import ssl

# Puertos soportados por el navegador
PUERTOS_SOPORTADOS = {80, 8080, 443, 3000, 5173}

class ClienteHTTP:
    def obtener_contenido(self, url, segundos_retraso=0, redirecciones=5):
        if redirecciones == 0:
            print("Error: Demasiadas redirecciones")
            return None

        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            print("URL inválida")
            return None

        protocol = parsed.scheme

        # Separar host y puerto desde netloc (soporta IPv4, dominios y IP:puerto)
        netloc = parsed.netloc

        # Detectar si hay puerto explícito en la URL
        # netloc puede ser: "dominio.cl", "123.123.123.123", "123.123.123.123:3000"
        if netloc.count(":") == 1:
            # tiene puerto explícito, ej: "35.209.140.243:3000"
            host, port_str = netloc.rsplit(":", 1)
            try:
                puerto = int(port_str)
            except ValueError:
                print("URL inválida: puerto no es un número")
                return None
        else:
            # sin puerto explícito: usar el predeterminado según protocolo
            host = netloc
            puerto = 443 if protocol == "https" else 80

        # Validar que el puerto esté soportado
        if puerto not in PUERTOS_SOPORTADOS:
            print(f"Conexión a puerto {puerto} no soportada")
            return ("error_puerto", f"Conexión a puerto {puerto} no soportada", None)

        ruta = parsed.path or "/"
        if parsed.query:
            ruta += "?" + parsed.query

        # Construir conexión según protocolo y puerto
        try:
            if protocol == "https" or puerto == 443:
                context = ssl._create_unverified_context()
                conn = http.client.HTTPSConnection(host, puerto, timeout=10, context=context)
            else:
                conn = http.client.HTTPConnection(host, puerto, timeout=10)
        except Exception as e:
            print(f"Error al crear conexión: {e}")
            return None

        print(f"Conectando a {host}:{puerto} con ruta {ruta}...")

        if segundos_retraso > 0:
            print(f"Esperando {segundos_retraso} segundos...")
            time.sleep(segundos_retraso)

        try:
            # El header Host debe incluir el puerto si no es el predeterminado
            host_header = netloc  # ya incluye puerto si fue especificado
            headers = {
                "Host": host_header,
                "User-Agent": "Navegador"
            }
            conn.request("GET", ruta, headers=headers)
            respuesta = conn.getresponse()

            # Manejo de redirecciones
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

    def coneccion(self, url, segundos_retraso=0):
        resultado = self.obtener_contenido(url, segundos_retraso)
        if resultado is None:
            return None

        status, reason, contenido = resultado
        print(f"Status: {status} {reason}")
        if contenido:
            print(contenido)
        return contenido