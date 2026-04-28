import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Clases.Pestaña import Pestana
import time


class MiNavegador:
    def __init__(self, root):
        self.root = root
        self.root.title("Navegador")
        self.root.attributes('-alpha', 0.0)
        self.root.geometry("0x0+0+0")
        
        self.app = tk.Toplevel(self.root)
        self.app.geometry("800x600")
        self.app.minsize(400, 300)
        
        # quita los bordes de cerrar, minimizar y maximizar
        self.app.overrideredirect(True)
        self.offset_x = 0
        self.offset_y = 0
        self.root.bind("<Unmap>", self.al_minimizar_desde_barra)
        self.root.bind("<Map>", self.al_restaurar_desde_barra)
        self.crear_barra_titulo()
        self.crear_barra_navegacion()
        self.crear_barra_estado()
        self.crear_area_contenido()

    def crear_barra_titulo(self):
        self.barra_titulo = tk.Frame(self.app, bg="#2c3e50", height=30)
        self.barra_titulo.pack(fill="x", side="top")
        lbl_titulo = tk.Label(self.barra_titulo, text=" navegador", 
                              bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        lbl_titulo.pack(side="left", padx=10)

        # para arrastrar la ventana
        self.barra_titulo.bind("<Button-1>", self.get_pos)
        self.barra_titulo.bind("<B1-Motion>", self.mover_ventana)

        # botones de control minimizar, maximizar y cerrar
        btn_cerrar = tk.Button(self.barra_titulo, text="✕", bg="#2c3e50", fg="#e74c3c", 
                               command=self.confirmar_cierre, bd=0, padx=10)
        
        btn_cerrar.pack(side="right")

        
        btn_max = tk.Button(self.barra_titulo, text="□", bg="#2c3e50", fg="white", 
                             command=self.alternar_maximizacion, bd=0, padx=10)
        btn_max.pack(side="right")

        btn_min = tk.Button(self.barra_titulo, text="—", bg="#2c3e50", fg="white", 
                             command=self.minimizar, bd=0, padx=10)
        btn_min.pack(side="right")

        self.cambio_color(btn_cerrar,"red","#2c3e50")
        self.cambio_color(btn_max,"gray","#2c3e50")
        self.cambio_color(btn_min,"gray","#2c3e50")
        
    def crear_barra_navegacion(self):
        self.frame_nav = tk.Frame(self.app, bg="#ecf0f1", pady=5)
        self.frame_nav.pack(fill="x")
        self.url_var = tk.StringVar()
        self.url_var.trace_add("write", self.validar_entrada)
        self.entrada_url = tk.Entry(self.frame_nav, textvariable=self.url_var)
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=10)
        self.entrada_url.insert(0, "file:///C:/ruta/tu_archivo.html")
        self.btn_ir = tk.Button(self.frame_nav, text="Ir", command=self.cargar_archivo)
        self.btn_ir.pack(side="right", padx=10)        
        self.validar_entrada()
        btn_nueva = tk.Button(self.frame_nav, text="+", width=3,command=self.nueva_pestana)
        btn_nueva.pack(side="right")

        btn_cerrar = tk.Button(self.frame_nav,text="✕",width=3,command=self.cerrar_pestana_actual)
        btn_cerrar.pack(side="right", padx=5)
        self.cambio_color(btn_cerrar,"red")


        self.btn_menu_color = tk.Menubutton(self.frame_nav, text="Colores",relief="raised", bg="#397daa")
        self.menu_colores = tk.Menu(self.btn_menu_color, tearoff=0)
        
        self.menu_colores.add_command(label="Color Blanco", command=lambda: self.cambiar_color_fondo("white", "black"))
        self.menu_colores.add_command(label="Color Beige", command=lambda: self.cambiar_color_fondo("#f4ecd8", "#5b4636"))
        self.menu_colores.add_command(label="Color Gris", command=lambda: self.cambiar_color_fondo("#A9A9A9", "black"))
        self.menu_colores.add_command(label="Color Negro", command=lambda: self.cambiar_color_fondo("#1e1e1e", "#dcdcdc"))
        
        self.btn_menu_color["menu"] = self.menu_colores
        self.btn_menu_color.pack(side="right", padx=10)

        # boton recargar
        self.btn_refresh = tk.Button(self.frame_nav, text="recargar")
        self.btn_refresh.config(command=self.cargar_archivo)
        time.sleep(60)
        self.btn_refresh.pack(side="right", padx=5)

        

    def cambiar_color_fondo(self, color_bg, color_fg):
        pestana = self.pestana_actual()      # obtiene la pestaña activa
        pestana.area_texto.config(
            bg=color_bg,
            fg=color_fg
        )
        self.estado.config(text="Esquema de color actualizado")

    def cambio_color(self, boton, nuevoColor, colorOriginal):
        boton.bind("<Enter>", lambda e: boton.config(bg=nuevoColor))
        boton.bind("<Leave>", lambda e: boton.config(bg=colorOriginal))

    def validar_entrada(self, *args):
            #si hay texto se activa el boton
            if self.url_var.get().strip():
                self.btn_ir.config(state="normal")
            else:
                self.btn_ir.config(state="disabled")

    def crear_barra_estado(self):
        self.frame_inferior = tk.Frame(self.app)
        self.frame_inferior.pack(side="bottom", fill="x")
        self.estado = tk.Label(self.frame_inferior, text="Listo", bd=1, relief="sunken", anchor="w")
        self.estado.pack(side="left", fill="x", expand=True)
        self.grip = ttk.Sizegrip(self.frame_inferior)
        self.grip.pack(side="right", anchor="se")

    def get_pos(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def mover_ventana(self, event):
        x = self.app.winfo_x() + event.x - self.offset_x
        y = self.app.winfo_y() + event.y - self.offset_y
        self.app.geometry(f"+{x}+{y}")

    def alternar_maximizacion(self):
        if self.app.state() == 'normal':
            self.app.state('zoomed')
        else:
            self.app.state('normal')

    def minimizar(self):
        self.root.iconify()

    def al_minimizar_desde_barra(self, event):
        if event.widget == self.root:
            self.app.withdraw()

    def al_restaurar_desde_barra(self, event):
        if event.widget == self.root:
            self.app.deiconify()

    def cargar_archivo(self):
        url = self.entrada_url.get().strip()
        pestana = self.pestana_actual()
        pestana.cargar_archivo(url, self.estado)

    def confirmar_cierre(self):
        if messagebox.askokcancel("Confirmar", "¿Seguro que quieres cerrar el navegador?"):
            self.root.destroy()

    def cambio_color(self, boton, nuevoColor, colorOriginal=None):
        if colorOriginal is None:
            colorOriginal = boton.cget("bg")

        boton.bind("<Enter>", lambda e: boton.config(bg=nuevoColor))
        boton.bind("<Leave>", lambda e: boton.config(bg=colorOriginal))

    def crear_area_contenido(self):
        self.notebook = ttk.Notebook(self.app)
        self.notebook.pack(fill="both", expand=True)

        self.pestanas = []
        self.nueva_pestana()
    
    def nueva_pestana(self):
        pestana = Pestana(self.notebook)
        self.pestanas.append(pestana)
     
    def pestana_actual(self):
        indice = self.notebook.index(self.notebook.select())
        return self.pestanas[indice]

    def cerrar_pestana_actual(self):
        if len(self.pestanas) == 1:
            return  # evita cerrar la última pestaña

        indice = self.notebook.index(self.notebook.select())
        pestana = self.pestanas[indice]

        pestana.cerrar()
        self.pestanas.pop(indice)