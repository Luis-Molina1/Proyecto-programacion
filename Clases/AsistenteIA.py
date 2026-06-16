import http.client
import socket
import json

class AsistenteIA:
    API_KEY= "" #no la subo a github pq se borra
    def __init__(self):
        modelo="gemini-3.5-flash"
        self.timeout= 10
        self.dominio= "generativelanguage.googleapis.com" 
        self.modelo= modelo 

    def procesar_comando(self, comando):
        if not comando.strip():
            return None, "comando vacio"
        
        ruta= f"/v1beta/models/{self.modelo}:generateContent?key={self.API_KEY}"
        prompt= f"Responde en formato HTML puro, sin ```html. Pregunta: {comando}"
        cuerpo= json.dumps({
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        })  
        try:
            conn= http.client.HTTPSConnection(self.dominio, timeout= self.timeout)
            conn.request("POST", ruta, body=cuerpo, headers={
                "Content-Type": "application/json", 
                "Host": self.dominio})
            respuesta= conn.getresponse()
            datos= respuesta.read().decode("utf-8")
            if respuesta.status != 200:
                return None, f"Error {respuesta.status}: {respuesta.reason}"
            respuesta= json.loads(datos)
            texto = respuesta["candidates"][0]["content"]["parts"][0]["text"].strip()
            if texto:
                return (texto, None) if texto else (None, "Gemini no generó respuesta")
        
        except socket.timeout:
            return None, "Tiempo de espera agotado (mas de 10 segundos)"
        except (ConnectionRefusedError, ConnectionError):
            return None, "No se pudo conectar a Gemini"
        except (KeyError, IndexError, json.JSONDecodeError):
            return None, "Gemini no genero ninguna respuesta"
        except Exception as e:
            return None, f"Error inesperado: {str(e)}"


"""
if __name__ == "__main__":
    asistente = AsistenteIA()
    pregunta = input("pregunta: ")
    respuesta = asistente.procesar_comando(pregunta)
    if respuesta:
        print(f"respuesta: \n{respuesta}")
"""