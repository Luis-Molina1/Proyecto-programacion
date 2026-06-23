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
            ],
            "top juegos 2026": [
                {"titulo": "Steam - Top juegos", "url": "https://store.steampowered.com", "descripcion": "Explora los juegos más populares y recomendados en Steam."},
                {"titulo": "Epic Games Store", "url": "https://store.epicgames.com", "descripcion": "Descubre los títulos destacados y tendencias del momento."},
                {"titulo": "Metacritic - Juegos del año", "url": "https://www.metacritic.com", "descripcion": "Reseñas y rankings sobre juegos destacados."},
                {"titulo": "IGN - Juegos", "url": "https://www.ign.com", "descripcion": "Noticias, reseñas y listas de los mejores juegos."}
            ],
            "recetas de pizza": [
                {"titulo": "Allrecipes - Pizza", "url": "https://www.allrecipes.com/search?q=pizza", "descripcion": "Recetas variadas de pizza para todos los gustos."},
                {"titulo": "RecetasGratis - Pizza", "url": "https://www.recetasgratis.net/buscar?q=pizza", "descripcion": "Ideas fáciles y rápidas para hacer pizza en casa."},
                {"titulo": "Food Network - Pizza", "url": "https://www.foodnetwork.com/search/pizza", "descripcion": "Recetas y consejos para preparar pizzas deliciosas."},
                {"titulo": "BBC Good Food - Pizza", "url": "https://www.bbcgoodfood.com/search?q=pizza", "descripcion": "Recetas clásicas y creativas de pizza."}
            ],
            "gatos": [
                {"titulo": "The Spruce Pets - Gatos", "url": "https://www.thesprucepets.com/cats-4162035", "descripcion": "Consejos y cuidados para gatos."},
                {"titulo": "Wikipedia - Gato", "url": "https://es.wikipedia.org/wiki/Gato", "descripcion": "Información general sobre la especie felina."},
                {"titulo": "Petfinder - Gatos", "url": "https://www.petfinder.com/search/cats-for-adoption", "descripcion": "Adopción y cuidado de gatos."},
                {"titulo": "Catster", "url": "https://www.catster.com", "descripcion": "Noticias, razas y consejos para gatos."}
            ],
            "como detectar la ia": [
                {"titulo": "Cómo detectar IA - Guía básica", "url": "https://www.google.com/search?q=como+detectar+ia", "descripcion": "Búsqueda general sobre señales para identificar contenido generado por IA."},
                {"titulo": "OpenAI - Detecting AI text", "url": "https://openai.com", "descripcion": "Recursos y referencias sobre detección y uso responsable de IA."},
                {"titulo": "Wikipedia - Inteligencia artificial", "url": "https://es.wikipedia.org/wiki/Inteligencia_artificial", "descripcion": "Información general sobre la IA y sus aplicaciones."}
            ],
            "como pasar el semestre": [
                {"titulo": "Cómo pasar el semestre - Consejos", "url": "https://www.google.com/search?q=como+pasar+el+semestre", "descripcion": "Ideas prácticas para organizar el estudio y mejorar el rendimiento."},
                {"titulo": "Estudiar mejor - Técnicas", "url": "https://www.google.com/search?q=tecnicas+de+estudio", "descripcion": "Métodos útiles para aprender más eficientemente."},
                {"titulo": "Productividad académica", "url": "https://www.google.com/search?q=productividad+estudiantil", "descripcion": "Estrategias para administrar el tiempo y estudiar mejor."}
            ],
            "cual es el mejor equipo de futbol": [
                {"titulo": "Google - Mejor equipo de fútbol", "url": "https://www.google.com/search?q=mejor+equipo+de+futbol", "descripcion": "Resultados generales sobre debates y rankings sobre el mejor equipo."},
                {"titulo": "ESPN - Fútbol", "url": "https://www.espn.com/soccer", "descripcion": "Noticias y clasificaciones de fútbol internacional."},
                {"titulo": "FIFA", "url": "https://www.fifa.com", "descripcion": "Información oficial sobre torneos y rankings mundiales."}
            ]
        }


    def obtener_pagina_principal(self):
        html = """
    <!DOCTYPE html>
    <html>
    <body>

    <center>

    <br><br><br>

    <h1>Super Meme Finder 🚀</h1>

    <br>

    <p>Busca cualquier cosa en el navegador</p>

    <br><br>

    <p>
    <input type="text" id="campoBusqueda" placeholder="Escribe tu búsqueda..." />
    </p>

    <p>
    <button onclick="buscar()">Buscar</button>
    </p>

    <br><br>

    <hr>

    <br>

    <h3>Sugerencias populares</h3>

    <ul>
    <li><a href="search://universidades en chile">Universidades en Chile</a></li>
    <li><a href="search://clima en mi ciudad">Clima en mi ciudad</a></li>
    <li><a href="search://locales de comida">Locales de comida</a></li>
    <li><a href="search://ultimos memes">Últimos memes</a></li>
    <li><a href="search://top juegos 2026">Top juegos 2026</a></li>
    <li><a href="search://gatos">Gatos</a></li>
    </ul>

    <br><br>

    <p>Hecho con Fe en cristo rey</p>

    </center>

    <script>
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
            <li>Top juegos 2026</li>
            <li>Recetas de pizza</li>
            <li>Gatos</li>
            <li>Como detectar la IA</li>
            <li>Como pasar el semestre</li>
            <li>Cual es el mejor equipo de futbol</li>
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
                <h3><a href=\"{resultado['url']}\" target=\"_blank\" rel=\"noopener noreferrer\">{resultado['titulo']}</a></h3>
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
