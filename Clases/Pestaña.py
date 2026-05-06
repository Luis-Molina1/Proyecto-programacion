import tkinter as tk
import os
import sys
from tkinter import messagebox
from Clases.Visor import VisorHTML
from Clases.Historial import Historial


class Pestana:
    def __init__(self, notebook, abrir_link, titulo="Nueva pestaña", bg="white", fg="black"):
        self.notebook = notebook
        self.frame = tk.Frame(notebook)
        self.abrir_link = abrir_link
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
        if not url.startswith("file:///") or not url.endswith((".html", ".htm")):
            messagebox.showerror(
                "Error",
                "Solo se permiten archivos locales con extensión .html o .htm"
            )
            self.estado_var.set("Error")
            return

        self.estado_var.set("Cargando...")
        self.text_widget.delete("1.0", tk.END)

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

            self.estado_var.set("Completado")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.estado_var.set("Error")


    def cerrar(self):
        self.notebook.forget(self.frame)
        self.frame.destroy()
    
    
    def obtener_nombre_archivo(self, url):
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

