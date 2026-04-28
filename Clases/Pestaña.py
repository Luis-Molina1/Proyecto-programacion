import tkinter as tk
import os
import sys
from tkinter import messagebox
from Clases.Visor import VisorHTML


class Pestana:
    def __init__(self, notebook,on_link_click, titulo="Nueva pestaña"):
        self.notebook = notebook
        self.frame = tk.Frame(notebook)
        self.on_link_click = on_link_click
        
        self.crear_barra_navegacion()

        self.area_texto = tk.Text(self.frame, bg="white", font=("Arial", 12))
        self.area_texto.pack(fill="both", expand=True)

        self.notebook.add(self.frame, text=titulo)
        self.notebook.select(self.frame)

        
        self.estado = tk.Label(
            self.frame,
            text="Listo",
            anchor="w",
            bg="#ecf0f1",
            padx=10
        )
        self.estado.pack(fill="x", side="bottom")



    def crear_barra_navegacion(self):
        self.frame_nav = tk.Frame(self.frame, bg="#ecf0f1", pady=5)
        self.frame_nav.pack(fill="x")

        self.url_var = tk.StringVar()
        self.entrada_url = tk.Entry(self.frame_nav, textvariable=self.url_var)
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=(10, 5))

        self.btn_ir = tk.Button(
            self.frame_nav,
            text="Ir",
            command=self.cargar_desde_barra
        )
        self.btn_ir.pack(side="left", padx=(0, 10))

    

    def cargar_desde_barra(self):
        url = self.url_var.get().strip()
        if not url:
            return
        self.cargar_archivo(url)




    def cargar_archivo(self, url):
        if not url.startswith("file:///") or not url.endswith((".html", ".htm") ):
            messagebox.showerror("Error", "Solo se permiten archivos locales de extencion html")
            return

        self.estado.config(text="Cargando...")
        self.area_texto.delete("1.0", tk.END)

        ruta = url.replace("file:///", "")
        if not sys.platform.startswith("win"):
            ruta = "/" + ruta

        if not os.path.exists(ruta):
            self.area_texto.insert(
                tk.END, f"No se encontró el archivo:\n{ruta}"
            )
            self.estado.config(text="Error")
            return

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            parser = VisorHTML(self.area_texto, self.on_link_click)
            parser.feed(contenido)
            
            nombre = self.obtener_nombre_archivo(url)
            self.notebook.tab(self.frame, text=f"{nombre}")

            self.estado.config(text="Completado")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.estado.config(text="Error")

    def cerrar(self):
        self.notebook.forget(self.frame)
    
    
    def obtener_nombre_archivo(self, url):
        nombre = os.path.basename(url.replace("file:///", ""))
        return nombre.replace(".html", "").replace(".htm", "")


