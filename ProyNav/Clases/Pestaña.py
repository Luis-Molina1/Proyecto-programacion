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
        
        self.area_texto = tk.Text(self.frame, bg="white", font=("Arial", 12))
        self.area_texto.pack(fill="both", expand=True)

        self.notebook.add(self.frame, text=titulo)
        self.notebook.select(self.frame)

    def cargar_archivo(self, url, estado_label):
        if not url.startswith("file:///") or not url.endswith((".html", ".htm") ):
            messagebox.showerror("Error", "Solo se permiten archivos locales de extencion html")
            return

        estado_label.config(text="Cargando...")
        self.area_texto.delete("1.0", tk.END)

        ruta = url.replace("file:///", "")
        if not sys.platform.startswith("win"):
            ruta = "/" + ruta

        if not os.path.exists(ruta):
            self.area_texto.insert(
                tk.END, f"No se encontró el archivo:\n{ruta}"
            )
            estado_label.config(text="Error")
            return

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            parser = VisorHTML(self.area_texto, self.on_link_click)
            parser.feed(contenido)
            
            nombre = self.obtener_nombre_archivo(url)
            self.notebook.tab(self.frame, text=f"{nombre}")

            estado_label.config(text="Completado")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            estado_label.config(text="Error")

    def cerrar(self):
        self.notebook.forget(self.frame)
    
    
    def obtener_nombre_archivo(self, url):
        nombre = os.path.basename(url.replace("file:///", ""))
        return nombre.replace(".html", "").replace(".htm", "")


