import unicodedata

class MotordeBusqueda:
    def __init__(self):
        self.busquedas_predefinidas = {
            "universidades en chile": [
                {"titulo": "Universidad de Chile", "url": "https://www.uchile.cl", "descripcion": "Sitio oficial de la Universidad de Chile."},
                {"titulo": "Pontificia Universidad Católica de Chile", "url": "https://www.uc.cl", "descripcion": "Página principal de la UC Chile."},
                {"titulo": "Universidad Católica de Valparaíso", "url": "https://www.ucv.cl", "descripcion": "Información sobre carreras y admisión UCV."},
                {"titulo": "Universidad de Santiago de Chile", "url": "https://www.usach.cl", "descripcion": "Portal oficial de la USACH."},
                {"titulo": "Universidad de Concepción", "url": "https://www.udec.cl", "descripcion": "Página de la Universidad de Concepción."},
                {"titulo": "Universidad Adolfo Ibáñez", "url": "https://www.uai.cl", "descripcion": "Información académica de la UAI."},
                {"titulo": "Universidad Técnica Federico Santa María", "url": "https://www.usm.cl", "descripcion": "Sitio oficial de la UTFSM."},
                {"titulo": "Universidad de los Andes Chile", "url": "https://www.uandes.cl", "descripcion": "Portal de la Universidad de los Andes."},
                {"titulo": "Universidad Austral de Chile", "url": "https://www.uach.cl", "descripcion": "Sitio formal de la Universidad Austral."},
                {"titulo": "Universidad de Valparaíso", "url": "https://www.uv.cl", "descripcion": "Página oficial de la Universidad de Valparaíso."}
            ],
            "clima en mi ciudad": [
                {"titulo": "Weather.com - Clima local", "url": "https://weather.com", "descripcion": "Pronóstico del tiempo para tu ciudad."},
                {"titulo": "AccuWeather - Clima hoy", "url": "https://www.accuweather.com", "descripcion": "Condiciones actuales y pronóstico extendido."},
                {"titulo": "Meteored Chile", "url": "https://www.meteored.cl", "descripcion": "Pronóstico meteorológico en Chile."},
                {"titulo": "Clima en Radar", "url": "https://www.climared.cl", "descripcion": "Información meteorológica local."},
                {"titulo": "Weather Underground", "url": "https://www.wunderground.com", "descripcion": "Informes y mapas de clima."},
                {"titulo": "MeteoChile", "url": "https://www.meteochile.cl", "descripcion": "Sitio chileno con datos de clima."},
                {"titulo": "Infoclima.cl", "url": "https://www.infoclima.cl", "descripcion": "Pronósticos y alertas meteorológicas."},
                {"titulo": "Clima YA", "url": "https://www.climaya.cl", "descripcion": "Reporte de tiempo para ciudades de Chile."},
                {"titulo": "Timeanddate - Weather", "url": "https://www.timeanddate.com/weather/", "descripcion": "Clima actual y previsiones por ciudad."},
                {"titulo": "MeteoBlue", "url": "https://www.meteoblue.com", "descripcion": "Clima detallado para cualquier ubicación."}
            ],
            "locales de comida": [
                {"titulo": "PedidosYa - Comida cerca", "url": "https://www.pedidosya.cl", "descripcion": "Encuentra locales de comida y delivery."},
                {"titulo": "Rappi - Restaurantes", "url": "https://www.rappi.com/cl", "descripcion": "Locales de comida cercanos en tu ciudad."},
                {"titulo": "Yapo.cl - Comida", "url": "https://www.yapo.cl/servicios", "descripcion": "Anuncios de locales y restaurantes."},
                {"titulo": "ChileMapas - Restaurantes", "url": "https://www.chilemapas.cl", "descripcion": "Listado de locales de comida en Chile."},
                {"titulo": "Restorando - Reservas", "url": "https://www.restorando.cl", "descripcion": "Encuentra restaurantes y haz reservas."},
                {"titulo": "Restaurantes.cl", "url": "https://www.restaurantes.cl", "descripcion": "Directorio de restaurantes y comida local."},
                {"titulo": "Guía McDonald's Chile", "url": "https://www.mcdonalds.cl", "descripcion": "Locales de comida rápida en Chile."},
                {"titulo": "OpenTable - Restaurantes", "url": "https://www.opentable.com", "descripcion": "Buscar y reservar restaurantes."},
                {"titulo": "Foursquare - Comida", "url": "https://es.foursquare.com", "descripcion": "Opiniones de locales de comida."},
                {"titulo": "Google Maps - Restaurantes", "url": "https://maps.google.com", "descripcion": "Encuentra locales de comida cercanos."}
            ],
            "ultimos memes": [
                {"titulo": "9GAG - Memes recientes", "url": "https://9gag.com", "descripcion": "Los memes más recientes de internet."},
                {"titulo": "Reddit - r/memes", "url": "https://www.reddit.com/r/memes", "descripcion": "Memes nuevos y populares de Reddit."},
                {"titulo": "Instagram - Memes", "url": "https://www.instagram.com/explore/tags/memes/", "descripcion": "Últimos memes compartidos en Instagram."},
                {"titulo": "Memedroid", "url": "https://www.memedroid.com", "descripcion": "Memes actualizados y tendencias."},
                {"titulo": "Imgur - Memes", "url": "https://imgur.com/t/memes", "descripcion": "Galería de memes recientes."},
                {"titulo": "TikTok - Memes", "url": "https://www.tiktok.com/tag/memes", "descripcion": "Videos de memes populares."},
                {"titulo": "Twitter - Memes", "url": "https://twitter.com/search?q=memes", "descripcion": "Búsqueda de memes actuales en Twitter."},
                {"titulo": "Memedroid Chile", "url": "https://www.memedroid.com/memes", "descripcion": "Colección de memes nuevos."},
                {"titulo": "Facebook - Memes", "url": "https://www.facebook.com/search/top?q=memes", "descripcion": "Memes compartidos recientemente."},
                {"titulo": "Know Your Meme", "url": "https://knowyourmeme.com", "descripcion": "Últimos memes y su contexto."}
            ]
        }

    def obtener_pagina_principal(self):
        """Retorna el HTML de la página principal del motor de búsqueda"""
        html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Buscador</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: #f0f0f0;
        }
        
        .contenedor {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .titulo {
            font-size: 64px;
            font-weight: bold;
            color: #333;
            margin-bottom: 50px;
        }
        
        .buscador {
            width: 100%;
            max-width: 500px;
            margin-bottom: 20px;
        }
        
        .buscador input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #333;
            border-radius: 5px;
            outline: none;
        }
        
        .boton-buscar {
            background-color: #333;
            color: white;
            padding: 12px 40px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .boton-buscar:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="titulo">Super Meme Finder</div>
        
        <div class="buscador">
            <input type="text" id="campoBusqueda" placeholder="Ingresa tu búsqueda..." />
        </div>
        
        <button class="boton-buscar" onclick="buscar()">Buscar</button>
    </div>
    
    <script>
        document.getElementById('campoBusqueda').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                buscar();
            }
        });
        
        function buscar() {
            var termino = document.getElementById('campoBusqueda').value;
            if (termino.trim()) {
                window.location.href = 'search://' + encodeURIComponent(termino.toLowerCase());
            }
        }
    </script>
</body>
</html>
        """
        return html

    def _normalizar_termino(self, termino):
        termino = termino.lower().strip()
        termino = unicodedata.normalize('NFKD', termino)
        termino = ''.join(ch for ch in termino if not unicodedata.combining(ch))
        return termino

    def obtener_resultados_busqueda(self, termino):
        termino_normalizado = self._normalizar_termino(termino)
        resultados = self.busquedas_predefinidas.get(termino_normalizado)

        if resultados is None:
            for clave, valor in self.busquedas_predefinidas.items():
                if termino_normalizado in clave or clave in termino_normalizado:
                    resultados = valor
                    break

        if resultados is None:
            return self._generar_sin_resultados(termino)
        return self._generar_resultados_html(termino, resultados)

    def _generar_sin_resultados(self, termino):
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado no encontrado</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background: #f0f0f0;
            padding: 40px;
            color: #333;
        }}
        .contenedor {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .titulo {{
            font-size: 32px;
            margin-bottom: 20px;
        }}
        .texto {{
            font-size: 16px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="titulo">No hay resultados para "{termino}"</div>
        <div class="texto">Usa uno de estos términos predefinidos:</div>
        <ul>
            <li>Universidades en Chile</li>
            <li>Clima en mi ciudad</li>
            <li>Locales de comida</li>
            <li>Ultimos memes</li>
        </ul>
    </div>
</body>
</html>
        """
        return html

    def _generar_resultados_html(self, termino, resultados):
        items_html = ""
        for resultado in resultados:
            items_html += f"""
            <div class=\"resultado\">
                <div class=\"url\">{resultado['url']}</div>
                <h3><a href=\"{resultado['url']}\">{resultado['titulo']}</a></h3>
                <p class=\"descripcion\">{resultado['descripcion']}</p>
            </div>
            """

        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados para {termino}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background: #f9f9f9;
            color: #333;
            padding: 20px;
        }}
        .contenedor {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .titulo {{
            font-size: 32px;
            margin-bottom: 20px;
        }}
        .resultado {{
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #ddd;
        }}
        .url {{
            color: #0073e6;
            font-size: 14px;
            margin-bottom: 4px;
        }}
        h3 {{
            margin: 0;
            font-size: 20px;
        }}
        h3 a {{
            color: #111;
            text-decoration: none;
        }}
        h3 a:hover {{
            text-decoration: underline;
        }}
        .descripcion {{
            font-size: 15px;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="titulo">Resultados para "{termino}"</div>
        {items_html}
    </div>
</body>
</html>
        """
        return html
