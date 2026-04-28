import tkinter as tk
from tkinter import messagebox
import os
import sys
from html.parser import HTMLParser


class VisorHTML(HTMLParser):
    def __init__(self, text_widget, on_link_click):
        super().__init__()
        self.text_widget = text_widget
        self.on_link_click = on_link_click
        self.etiquetas_activas = []
        
        self.text_widget.tag_configure("h1", font=("Arial", 16, "bold"))
        self.text_widget.tag_configure("h2", font=("Arial", 14, "bold"))
        self.text_widget.tag_configure("b", font=("Arial", 12, "bold"))
        self.text_widget.tag_configure("i", font=("Arial", 12, "italic"))
        self.text_widget.tag_configure("a", foreground="blue", underline=True)
        
        self.link_counter = 0
        self.current_link_url = ""
        self.current_link_tag = ""

    def handle_starttag(self, tag, attrs):
        self.etiquetas_activas.append(tag)
        if tag in ['p', 'h1', 'h2', 'br', 'li']:
            self.text_widget.insert(tk.END, "\n")
        elif tag == 'a':
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict:
                self.link_counter += 1
                self.current_link_tag = f"link_{self.link_counter}"
                self.current_link_url = attrs_dict['href']

    def handle_endtag(self, tag):
        if tag in self.etiquetas_activas:
            for i in reversed(range(len(self.etiquetas_activas))):
                if self.etiquetas_activas[i] == tag:
                    self.etiquetas_activas.pop(i)
                    break
        if tag in ['p', 'h1', 'h2', 'li']:
            self.text_widget.insert(tk.END, "\n")
        elif tag == 'a':
            self.current_link_tag = ""
            self.current_link_url = ""

    def handle_data(self, data):
        texto = data.strip()
        if not texto:
            return
        estilos_a_aplicar = [t for t in self.etiquetas_activas if t in ["h1", "h2", "b", "i"]]
        
        if 'a' in self.etiquetas_activas and self.current_link_tag:
            estilos_a_aplicar.append("link")
            estilos_a_aplicar.append(self.current_link_tag)
            
            url = self.current_link_url
            self.text_widget.tag_bind(self.current_link_tag, "<Button-1>", lambda e, u=url: self.on_link_click(u))
            self.text_widget.tag_bind(self.current_link_tag, "<Enter>", lambda e: self.text_widget.config(cursor="hand2"))
            self.text_widget.tag_bind(self.current_link_tag, "<Leave>", lambda e: self.text_widget.config(cursor=""))
            
        self.text_widget.insert(tk.END, texto + " ", estilos_a_aplicar)

class MiNavegador:
    def __init__(self, root):
        self.root = root
        self.root.title("Navegador Universitario")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)
        
        # quita los bordes de cerrar, minimizar y maximizar
        self.root.overrideredirect(True)
        self.offset_x = 0
        self.offset_y = 0
        self.crear_barra_titulo()
        self.crear_barra_navegacion()
        self.crear_area_contenido()
        self.crear_barra_estado()

    def crear_barra_titulo(self):
        self.barra_titulo = tk.Frame(self.root, bg="#2c3e50", height=30)
        self.barra_titulo.pack(fill="x", side="top")
        lbl_titulo = tk.Label(self.barra_titulo, text=" navegador", 
                              bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        lbl_titulo.pack(side="left", padx=10)

        # para arrastrar la ventana
        self.barra_titulo.bind("<Button-1>", self.get_pos)
        self.barra_titulo.bind("<B1-Motion>", self.mover_ventana)

        # botones de control minimizar, maximizar y cerrar
        btn_cerrar = tk.Button(self.barra_titulo, text="✕", bg="#e74c3c", fg="white", 
                               command=self.confirmar_cierre, bd=0, padx=10)
        btn_cerrar.pack(side="right")
        
        btn_max = tk.Button(self.barra_titulo, text="□", bg="#2c3e50", fg="white", 
                             command=self.alternar_maximizacion, bd=0, padx=10)
        btn_max.pack(side="right")
        
        btn_min = tk.Button(self.barra_titulo, text="—", bg="#2c3e50", fg="white", 
                             command=self.minimizar, bd=0, padx=10)
        btn_min.pack(side="right")

    def crear_barra_navegacion(self):
        self.frame_nav = tk.Frame(self.root, bg="#ecf0f1", pady=5)
        self.frame_nav.pack(fill="x")
        self.entrada_url = tk.Entry(self.frame_nav)
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=10)
        self.entrada_url.insert(0, "file:///C:/ruta/tu_archivo.html")
        self.btn_ir = tk.Button(self.frame_nav, text="Ir", command=self.cargar_archivo)
        self.btn_ir.pack(side="right", padx=10)

    def crear_area_contenido(self):
        self.area_texto = tk.Text(self.root, bg="white", font=("Arial", 12))
        self.area_texto.pack(fill="both", expand=True, padx=5, pady=5)

    def crear_barra_estado(self):
        self.estado = tk.Label(self.root, text="Listo", bd=1, relief="sunken", anchor="w")
        self.estado.pack(side="bottom", fill="x")
    
    def get_pos(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def mover_ventana(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def alternar_maximizacion(self):
        if self.root.state() == 'normal':
            self.root.state('zoomed')
        else:
            self.root.state('normal')

    def minimizar(self):
        self.root.overrideredirect(False) #para que aparezca en la barra de tareas
        self.root.iconify()
        self.root.bind("<FocusIn>", lambda e: self.root.overrideredirect(True))

    def cargar_archivo(self):
        url = self.entrada_url.get().strip()
        if not url.startswith("file:///"):
            messagebox.showerror("Error", "Solo se permiten archivos locales")
            return
        
        self.estado.config(text="Cargando...")
        self.area_texto.delete('1.0', tk.END)
        self.area_texto.insert(tk.END, f"Simulando carga de: {url}\n")
        self.estado.config(text="Listo")
        
        #PARTE NUEVA (lee el archivo real y lo muestra)
        ruta_archivo = url.replace("file:///", "")
        
        #en sistemas mac o linux, la ruta debe empezar con /
        if not sys.platform.startswith("win"):
            ruta_archivo = "/" + ruta_archivo

        #verificamos si existe el archivo
        if not os.path.exists(ruta_archivo): ## 
            self.area_texto.insert(tk.END, f"Error: No se encontró el archivo en:\n{ruta_archivo}")
            self.estado.config(text="Error de carga")
            return

        #leemos el archivo y usamos nuestro parser nativo
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                
            parser = VisorHTML(self.area_texto, self.manejar_clic_enlace)
            parser.feed(contenido)
            self.estado.config(text="Completado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
            self.estado.config(text="Error")

    def manejar_clic_enlace(self, url_destino):
        if url_destino.startswith("http://") or url_destino.startswith("https://"):
            messagebox.showinfo("Enlace no soportado", f"Actualmente el navegador no soporta carga de sitios web externos:\n{url_destino}")
            return
            
        if url_destino.startswith("file:///"):
            nueva_url = url_destino
        else:
            url_actual = self.entrada_url.get().strip()
            ruta_actual = url_actual.replace("file:///", "")
            if not sys.platform.startswith("win") and not ruta_actual.startswith("/"):
                ruta_actual = "/" + ruta_actual
                
            ruta_base = os.path.dirname(ruta_actual)
            nueva_ruta = os.path.join(ruta_base, url_destino)
            nueva_ruta_normalizada = os.path.normpath(nueva_ruta)
            nueva_url = "file:///" + nueva_ruta_normalizada.replace("\\", "/")
            
        self.entrada_url.delete(0, tk.END)
        self.entrada_url.insert(0, nueva_url)
        self.cargar_archivo()

    def confirmar_cierre(self):
        if messagebox.askokcancel("Confirmar", "¿Seguro que quieres cerrar el navegador?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MiNavegador(root)
    root.mainloop()