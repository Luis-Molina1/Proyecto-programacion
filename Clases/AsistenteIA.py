import http.client
import json

class AsistenteIA:
    # Lee la clave desde el archivo de texto simple
    with open("api_key.txt", "r") as f:
        API_KEY = f.read().strip()
    def __init__(self):
        modelo="gemini-2.5-flash"
        self.timeout= 10
        self.dominio= "generativelanguage.googleapis.com" 
        self.modelo= modelo 

    def procesar_comando(self, comando):
        if not comando.strip():
            return None, "comando vacio"
        
        ruta= f"/v1beta/models/{self.modelo}:generateContent?key={self.API_KEY}"
        prompt= f"responde en formato HTML y no pongas textualmente que estas respondiewndo en html. Pregunta: {comando}"
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
        
        except TimeoutError:
            return None, "tiempo de espera agotado"
        except (KeyError, IndexError):
            return None, "gemini no genero ninguna respuesta"
        except Exception as e:
            return None, f"error inesperado {e}"
        


"""
if __name__ == "__main__":
    asistente = AsistenteIA()
    pregunta = input("pregunta: ")
    respuesta = asistente.procesar_comando(pregunta)
    if respuesta:
        print(f"respuesta: \n{respuesta}")
"""