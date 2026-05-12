import tkinter as tk
import os
import sys
import urllib.parse
from tkinter import messagebox
from Clases.Visor import VisorHTML
from Clases.Historial import Historial
from Clases.ClienteHTTP import ClienteHTTP


class Pestana:
    def __init__(self, notebook, abrir_link, titulo="Nueva pestaña", bg="white", fg="black", on_historial_update=None):
        self.notebook = notebook
        self.frame = tk.Frame(notebook)
        self.abrir_link = abrir_link
        self.on_historial_update = on_historial_update
        self.historial = Historial()
        
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
        self.text_widget.delete("1.0", tk.END)
        self.visor.reset()

        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https"):
            resultado = ClienteHTTP().obtener_contenido(url, segundos_retraso=0)
            
            # si fallo la conexion https intentamos por http
            if resultado is None and url.startswith("https://"):
                url_fallback = url.replace("https://", "http://", 1)
                resultado = ClienteHTTP().obtener_contenido(url_fallback, segundos_retraso=0)
                if resultado is not None:
                    url = url_fallback
                    self.url_var.set(url)  # actualiza la barra de direcciones con http

            if resultado is None:
                self.text_widget.insert(tk.END, f"No se pudo cargar la página:\n{url}")
                self.estado_var.set("Error")
                return

            _, _, contenido = resultado
            self.visor.feed(contenido)

            nombre = self.obtener_nombre_archivo(url)
            self.notebook.tab(self.frame, text=nombre)

            if hasattr(self, "historial"):
                self.historial.agregar(url, nombre)

            if self.on_historial_update:
                self.on_historial_update()

            self.estado_var.set("Completado")
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
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # usar el visor ya creado
            self.visor.feed(contenido)

            # actualizar título de la pestaña
            nombre = os.path.basename(ruta)
            self.notebook.tab(self.frame, text=nombre)

            # historial (si existe)
            if hasattr(self, "historial"):
                self.historial.agregar(url, nombre)

            if self.on_historial_update:
                self.on_historial_update()

            self.estado_var.set("Completado")

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

        # si no tiene http, https, file, al inicio y si un nombre.algo lo buscara
        parsed = urllib.parse.urlparse(url)
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

        self.text_widget = tk.Text(self.frame_contenido, wrap="word")
        self.text_widget.pack(fill="both", expand=True)

        self.visor = VisorHTML(
            self.text_widget,
            on_link_click=self.abrir_link
        )

    
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

