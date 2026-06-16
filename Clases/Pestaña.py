import re
import html
import tkinter as tk
import os
import sys
import urllib.parse
from tkinter import messagebox
from Clases.Visor import VisorHTML
from Clases.Historial import Historial
from Clases.ClienteHTTP import ClienteHTTP
from Clases.AsistenteIA import AsistenteIA

class Pestana:
    def __init__(self, notebook, abrir_link, titulo="Nueva pestaña", bg="white", fg="black", on_historial_update=None, on_navegacion=None, navegador=None):
        self.notebook = notebook
        self.frame = tk.Frame(notebook)
        self.abrir_link = abrir_link
        self.on_historial_update = on_historial_update
        self.on_navegacion = on_navegacion
        self.navegador = navegador
        self.historial = Historial()
        self.asistente = AsistenteIA()

        self.historial_atras = []
        self.historial_adelante = []
        
        self.area_texto = tk.Text(self.frame, bg=bg, fg=fg, font=("Arial", 12))
        
        self.abrir_link = abrir_link
        self.notebook.add(self.frame, text=titulo)
        self.notebook.select(self.frame)
        self.crear_barra_local()
        self.crear_contenido()
        self.crear_barra_estado()
        self.aplicar_color(bg, fg)
    
    def obtener_url(self):
        return self.url_var.get()

    def cargar_archivo(self, url):
        self.estado_var.set("Cargando...")
        try:
            # forzar actualización de la UI antes de operaciones bloqueantes
            self.frame.update_idletasks()
            self.frame.update()
        except Exception:
            pass
        self.text_widget.delete("1.0", tk.END)
        self.visor.reset()

        if hasattr(self, "navegador") and self.navegador and self.navegador.modo_offline.get():
            parsed= urllib.parse.urlparse(url)
            if parsed.scheme in ("http", "https"):
                self.text_widget.insert(tk.END, "Navegador en MODO OFFLINE, cambia de modo para cargar esta página")
                self.estado_var.set("MODO OFFLINE activo")
                if hasattr(self.navegador, "actualizar_botones_navegacion"):
                    self.navegador.actualizar_botones_navegacion()
                return

        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https"):
            try:
                # mostrar estado y forzar redraw antes de la petición
                self.estado_var.set("Cargando...")
                self.frame.update_idletasks()
                self.frame.update()
            except Exception:
                pass
            resultado = ClienteHTTP().obtener_contenido(url, segundos_retraso=0)
            
            # si fallo la conexion https intentamos por http
            if resultado is None and url.startswith("https://"):
                url_fallback = url.replace("https://", "http://", 1)
                resultado = ClienteHTTP().obtener_contenido(url_fallback, segundos_retraso=0)
                if resultado is not None:
                    url = url_fallback
                    # actualiza la barra de direcciones con http
                    self.url_var.set(url)

            if resultado is None:
                self.text_widget.insert(tk.END, f"No se pudo cargar la página:\n{url}")
                self.estado_var.set("Error")
                return

            _, _, contenido = resultado
            estatus, razon, contenido = resultado
            self.visor.feed(contenido)


            match_dominio = re.search(r"(https?)://([^/]+)", url)
            nombre = match_dominio.group(2) if match_dominio else url
            match_titulo = re.search(r"<title>(.*?)</title>", contenido, re.IGNORECASE | re.DOTALL)
            if match_titulo:
                titulo_extraido = html.unescape(match_titulo.group(1).strip())
                if titulo_extraido:
                    nombre = titulo_extraido
            if len(nombre) > 25:
                nombre = nombre[:25] + "..."
            self.notebook.tab(self.frame, text=nombre)

            if hasattr(self, "historial"):
                self.historial.agregar(url, nombre)

            if self.on_historial_update:
                self.on_historial_update()
            self.estado_var.set(f"{estatus} {razon}")
            if self.on_navegacion:
                self.on_navegacion()

                # se actualizan los botones de navegacion para online
            if self.navegador and hasattr(self.navegador, "actualizar_botones_navegacion"):
                self.navegador.actualizar_botones_navegacion()
            return
        
        ruta = url.replace("file:///", "")
        if not sys.platform.startswith("win"):
            ruta = "/" + ruta

        if not os.path.exists(ruta):
            self.text_widget.insert(
                tk.END, f"No se encontró el archivo:\n{ruta}"
            )
            self.estado_var.set("Error")
            return

        try:
            try:
                # forzar que el estado se muestre antes de leer archivo local
                self.estado_var.set("Cargando...")
                self.frame.update_idletasks()
                self.frame.update()
            except Exception:
                pass
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # usar el visor ya creado
            self.visor.feed(contenido)

            # intentar extraer <title> del contenido (para archivos locales)
            titulo_extraido = None
            match_titulo = re.search(r"<title>(.*?)</title>", contenido, re.IGNORECASE | re.DOTALL)
            if match_titulo:
                titulo_extraido = html.unescape(match_titulo.group(1).strip())

            # determinar nombre a mostrar en la pestaña
            if titulo_extraido:
                nombre = titulo_extraido
            else:
                nombre = os.path.basename(ruta)

            # si la pestaña ya tenía un título personalizado (no 'Nueva pestaña'), preferirlo
            try:
                tab_actual = self.notebook.tab(self.frame, "text")
            except Exception:
                tab_actual = None

            if tab_actual and tab_actual != "Nueva pestaña":
                # si encontramos un título en el HTML, úsalo; si no, mantenemos el título existente
                display_name = nombre if titulo_extraido else tab_actual
            else:
                display_name = nombre

            if len(display_name) > 25:
                display_name = display_name[:25] + "..."

            self.notebook.tab(self.frame, text=display_name)

            # historial (si existe)
            if hasattr(self, "historial"):
                self.historial.agregar(url, display_name)

            if self.on_historial_update:
                self.on_historial_update()

            self.estado_var.set("Completado")
            # se actualizan los botones de navegacion para local
            if self.navegador and hasattr(self.navegador, "actualizar_botones_navegacion"):
                self.navegador.actualizar_botones_navegacion()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.estado_var.set("Error")


    def cerrar(self):
        self.notebook.forget(self.frame)
        self.frame.destroy()
    
    
    def obtener_nombre_archivo(self, url):
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https"):
            nombre = os.path.basename(parsed.path)
            if nombre:
                return nombre.replace(".html", "").replace(".htm", "")
            return parsed.netloc

        nombre = os.path.basename(url.replace("file:///", ""))
        return nombre.replace(".html", "").replace(".htm", "")

    def crear_barra_local(self):
        self.frame_nav = tk.Frame(self.frame)
        self.frame_nav.pack(fill="x")
        
        self.url_var = tk.StringVar(
                value="file:///C:/ruta/tu_archivo.html"
            )


        self.entry_url = tk.Entry(self.frame_nav, textvariable=self.url_var)
        self.entry_url.pack(side="left", fill="x", expand=True, padx=5, pady=2)
        self.btn_ir = tk.Button(self.frame_nav, text="Ir", command=self.cargar)
        self.btn_ir.pack(side="left", padx=5)
        self.url_var.trace_add("write", self.validar_entrada)
        self.validar_entrada()

        self.frame_ia = tk.Frame(self.frame)
        self.frame_ia.pack(fill="x")
        self.ia_var = tk.StringVar()
        self.entry_ia = tk.Entry(self.frame_ia, textvariable=self.ia_var)
        self.entry_ia.pack(side="left", fill="x", expand=True, padx=5, pady=2)
        self.entry_ia.bind("<Return>", lambda e: self.consultar_ia())
        self.btn_ia = tk.Button(self.frame_ia, text="IA", command=self.consultar_ia)
        self.btn_ia.pack(side="left", padx=2)

    def validar_entrada(self, *args):
            #si hay texto se activa el boton
            if self.url_var.get().strip():
                self.btn_ir.config(state="normal")
            else:
                self.btn_ir.config(state="disabled")

    def crear_barra_estado(self):
        self.estado_var = tk.StringVar(value="Listo")

        self.barra_estado = tk.Label(
            self.frame,
            textvariable=self.estado_var,
            anchor="w",
            bg="#eeeeee"
        )
        self.barra_estado.pack(fill="x", side="bottom")


    def cargar(self):
        url = self.url_var.get().strip()
        if not url:
            self.estado_var.set("URL vacía")
            return
        
        if hasattr(self, "historial") and self.historial.entradas:
            url_actual = self.historial.entradas[-1][0]
            if url_actual != url:
                self.historial_atras.append(url_actual)
                self.historial_adelante = []

        # si es una búsqueda interna, enviar al navegador para procesarla
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme == "search":
            self.abrir_link(url)
            return

        # si no tiene http, https, file, al inicio y si un nombre.algo lo buscara
        if not parsed.scheme and not os.path.isabs(url):
            if "." in url and " " not in url:
                url = "https://" + url
                self.url_var.set(url)

        self.cargar_archivo(url)


    def recargar(self):
        if not self.historial.entradas:
            self.estado_var.set("No hay historial para recargar")
            return

        url = self.historial.entradas[-1][0]
        self.url_var.set(url)
        self.cargar_archivo(url)


    def actualizar_estado(self, texto):
        self.estado_var.set(texto)


    def crear_contenido(self):
        self.frame_contenido = tk.Frame(self.frame)
        self.frame_contenido.pack(fill="both", expand=True)
        self.barra_desplazamiento = tk.Scrollbar(self.frame_contenido, orient="vertical")
        self.barra_desplazamiento.pack(side="right", fill="y")
        self.text_widget = tk.Text(self.frame_contenido, wrap="word", yscrollcommand=lambda inicio, fin: self.auto_desplazamiento(self.barra_desplazamiento, inicio, fin))
        self.barra_desplazamiento.config(command=self.text_widget.yview)    
        self.text_widget.pack(fill="both", expand=True)
        self.visor = VisorHTML(
            self.text_widget,
            on_link_click=self.abrir_link,
            pestana=self
        )
    def auto_desplazamiento(self, barra, inicio, fin):
        if float(inicio) <= 0.0 and float(fin) >= 1.0:
            barra.config(width=0)
        else:
            barra.config(width=16)
        barra.set(inicio, fin)
    
    def aplicar_color(self, bg, fg):
        # fondo de la pestaña
        self.frame.config(bg=bg)

        # barra de navegación
        self.frame_nav.config(bg=bg)
        self.entry_url.config(bg="white", fg="black")
        self.btn_ir.config(bg=bg, fg=fg)

        # área de contenido
        self.frame_contenido.config(bg=bg)
        self.text_widget.config(bg=bg, fg=fg, insertbackground=fg)

        # barra de estado
        self.barra_estado.config(bg=bg, fg=fg)


    def ir_atras(self):
        # si no hay historial atras, muestra mensaje
        if not self.historial_atras:
            self.estado_var.set("No hay paginas atras")
            return
        
        url_pasada = self.historial_atras.pop()
        if self.historial.entradas:
            url_actual = self.historial.entradas[-1][0]
            self.historial_adelante.append(url_actual)
            
        self.url_var.set(url_pasada)
        self.cargar_archivo(url_pasada)

    def ir_adelante(self):
        # si no hay historial adelante, muestra mensaje
        if not self.historial_adelante:
            self.estado_var.set("No hay pagina siguiente")
            return

        url_futura = self.historial_adelante.pop()
        if self.historial.entradas:
            url_actual = self.historial.entradas[-1][0]
            self.historial_atras.append(url_actual)

        self.url_var.set(url_futura)
        self.cargar_archivo(url_futura)

    def consultar_ia(self):
        comando= self.ia_var.get().strip()
        if not comando:
            self.estado_var.set("comando vacio, escriba un comando")
            return
        self.estado_var.set("preguntando a gemini....")
        self.btn_ia.config(state="disabled")
        self.frame.update()
        
        respuesta, error = self.asistente.procesar_comando(comando)
        self.btn_ia.config(state="normal")
        self.visor.reset()
        self.text_widget.delete("1.0", tk.END)
        if error:
            self.visor.feed(f"<h2>Error</h2><p>{error}</p>")
            self.estado_var.set(f"Error: {error}")
            return
        self.visor.feed(f"{respuesta}")
        self.ia_var.set("")
        self.estado_var.set("respuesta recibida")