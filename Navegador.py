import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Clases.Pestaña import Pestana


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
        self.frame_nav = tk.Frame(self.root, bg="#ecf0f1", pady=5)
        self.frame_nav.pack(fill="x")
        self.entrada_url = tk.Entry(self.frame_nav)
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=10)
        self.entrada_url.insert(0, "file:///C:/ruta/tu_archivo.html")
        self.btn_ir = tk.Button(self.frame_nav, text="Ir", command=self.cargar_archivo)
        self.btn_ir.pack(side="right", padx=10)        
        btn_nueva = tk.Button(
            self.frame_nav, text="+", width=3,
            command=self.nueva_pestana
        )
        btn_nueva.pack(side="right")
        
        btn_cerrar = tk.Button(
            self.frame_nav,
            text="✕",
            width=3,
            command=self.cerrar_pestana_actual
        )
        btn_cerrar.pack(side="right", padx=5)
        self.cambio_color(btn_cerrar,"red")


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
        self.notebook = ttk.Notebook(self.root)
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
