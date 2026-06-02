import http.client
import json

class AsistenteIA:
    def __init__(self, api_key):
        self.api_key = api_key
        self.timeout = 10
        self.dominio = "generativelanguage.googleapis.com"        
    def procesar_comando(self):
        ruta = f"/v1beta/interactions"
        cuerpo = json.dumps({
            "contents": [
                {
                    "parts": [{"text": "w"}]
                }
            ]
            
        })  