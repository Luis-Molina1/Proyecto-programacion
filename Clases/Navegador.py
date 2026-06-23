import os
import tempfile
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from urllib.parse import urljoin, urlparse, unquote
from Clases.Pestaña import Pestana
from Clases.Historial import Historial
from Clases.Favoritos import Favoritos
from Clases.MotordeBusqueda import MotordeBusqueda

class MiNavegador:
    def __init__(self, root):
        self.root = root
        self.root.title("Navegador")
        self.root.attributes('-alpha', 0.0)
        self.root.geometry("0x0+0+0")
        self.color_bg_actual = "white"
        self.color_fg_actual = "black"
        
        self.app = tk.Toplevel(self.root)
        self.app.geometry("800x600")
        self.app.minsize(400, 300)

        self.modo_offline= tk.BooleanVar(value=False)

        
        # quita los bordes de cerrar, minimizar y maximizar
        self.app.overrideredirect(True)
        self.offset_x = 0
        self.offset_y = 0
        self.root.bind("<Unmap>", self.al_minimizar_desde_barra)
        self.root.bind("<Map>", self.al_restaurar_desde_barra)
        self.favoritos = Favoritos()
        self.app.bind("<Control-Tab>", self.siguiente_pestana)
        self.app.bind("<Control-Shift-Tab>", self.pestana_anterior)
        self.app.bind("<Control-w>", lambda e: self.cerrar_pestana_actual())
        self.app.bind("<Control-z>", lambda e: self.nueva_pestana())
        for i in range(1, 10):
            self.app.bind(f"<Control-Key-{i}>", lambda e, idx=i-1: self.ir_a_pestana(idx))
        self.crear_barra_titulo()
        self.crear_barra_navegacion()
        self.crear_area_contenido()
        self.crear_barra_estado()
        
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_historial = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Historial", menu=self.menu_historial)
        
        self.menu_fav = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Favoritos", menu=self.menu_fav)

        self.actualizar_menu_historial()
        self.actualizar_menu_fav()

        self.btn_atras = tk.Button(self.frame_nav, text="❮", width=3, command=self.retroceder_pag, state="disabled")
        self.btn_atras.pack(side="left", padx=3)
        self.btn_adelante = tk.Button(self.frame_nav, text="❯", width=3, command=self.avanzar_pag, state="disabled")
        self.btn_adelante.pack(side="left", padx=3)
        

    def crear_barra_titulo(self):
        self.barra_titulo = tk.Frame(self.app, bg="#2c3e50", height=30)
        self.barra_titulo.pack(fill="x", side="top")
        self.lbl_titulo = tk.Label(self.barra_titulo, text="🌐 Super Ultra Mega Navegador v99999 No Fake", 
                              bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        self.lbl_titulo.pack(side="left", padx=10)

        # para arrastrar la ventana
        self.barra_titulo.bind("<Button-1>", self.get_pos)
        self.barra_titulo.bind("<B1-Motion>", self.mover_ventana)

        # botones de control minimizar, maximizar y cerrar
        # Función auxiliar para hover moderno
        def aplicar_hover(btn, color_normal, color_hover):
            btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
            btn.bind("<Leave>", lambda e: btn.config(bg=color_normal))


        # ===== BOTÓN CERRAR =====
        btn_cerrar = tk.Button(
            self.barra_titulo,
            text="✕",
            bg="#2c3e50",
            fg="#e74c3c",
            command=self.confirmar_cierre,
            bd=0,
            padx=12,
            pady=4,
            font=("Segoe UI", 10),
            cursor="hand2",
            activebackground="#e74c3c",
            activeforeground="white"
        )
        btn_cerrar.pack(side="right")

        aplicar_hover(btn_cerrar, "#2c3e50", "#c0392b")


        # ===== BOTÓN MAXIMIZAR =====
        btn_max = tk.Button(
            self.barra_titulo,
            text="□",
            bg="#2c3e50",
            fg="white",
            command=self.alternar_maximizacion,
            bd=0,
            padx=12,
            pady=4,
            font=("Segoe UI", 10),
            cursor="hand2",
            activebackground="#4a90e2",
            activeforeground="white"
        )
        btn_max.pack(side="right")

        aplicar_hover(btn_max, "#2c3e50", "#3a3a3a")


        # ===== BOTÓN MINIMIZAR =====
        btn_min = tk.Button(
            self.barra_titulo,
            text="—",
            bg="#2c3e50",
            fg="white",
            command=self.minimizar,
            bd=0,
            padx=12,
            pady=4,
            font=("Segoe UI", 10),
            cursor="hand2",
            activebackground="#4a90e2",
            activeforeground="white"
        )
        btn_min.pack(side="right")

        aplicar_hover(btn_min, "#2c3e50", "#3a3a3a")


        
    def crear_barra_navegacion(self):
        self.frame_nav = tk.Frame(self.app, bg="#ecf0f1", pady=5)
        self.frame_nav.pack(fill="x")

        btn_nueva = tk.Button(self.frame_nav, text="+", width=3,command=self.nueva_pestana)
        btn_nueva.pack(side="right")

        self.btn_estrella_fav = tk.Button(self.frame_nav, text="☆", command=self.guardar_en_fav, bg="#ffcc00")
        self.btn_estrella_fav.pack(side="left", padx=5)


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

        
        self.btn_menu_principal = tk.Menubutton(
            self.frame_nav,
            text="Menu",
            bg="#5d98d3",
            relief=tk.RAISED
        )

        self.menu_principal = tk.Menu(self.btn_menu_principal, tearoff=0, bd=1)
        self.btn_menu_principal["menu"] = self.menu_principal

        self.menu_fav_principal = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Favoritos", menu=self.menu_fav_principal)

        self.menu_hist_principal = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Historial", menu=self.menu_hist_principal)

        self.btn_menu_principal.pack(side=tk.LEFT, padx=5)

        # boton recargar
        self.btn_refresh = tk.Button(self.frame_nav, text="recargar", command=self.ejecutar_refresh)
        self.btn_refresh.pack(side="right", padx=5)

        self.chk_offline = tk.Checkbutton(
            self.frame_nav, 
            text="Modo Offline", 
            variable=self.modo_offline,
            onvalue=True, 
            offvalue=False,
            command=self.notificar_cambio_modo
        )
        self.chk_offline.pack(side="right", padx=10)
        # boton MemeFinder -> abre la página principal del Motor de Búsqueda en una nueva pestaña interna
        self.btn_memefinder = tk.Button(self.frame_nav, text="MemeFinder", command=self.abrir_memefinder)
        self.btn_memefinder.pack(side="right", padx=5)

    def ejecutar_refresh(self):
        self.estado.config(text="Recargando...")
        self.btn_refresh.config(state="disabled")
        self.app.config(cursor="watch")
        self.app.update_idletasks()
        self.root.after(1000, self.finalizar_refresh)


    def finalizar_refresh(self):
        self.recargar_pestana()
        self.estado.config(text="Página actualizada", fg="black")
        self.btn_refresh.config(state="normal")
        self.app.config(cursor="")
        self.root.after(2000, lambda: self.estado.config(text="Listo"))

    def abrir_memefinder(self):
        """Crea una nueva pestaña interna y carga la página principal del Motor de Búsqueda."""
        try:
            # Crear nueva pestaña y obtener la pestaña actual
            self.nueva_pestana("Super Meme Finder")
            pestana = self.obtener_pestana_actual()

            # Generar HTML del motor de búsqueda
            motor = MotordeBusqueda()
            html = motor.obtener_pagina_principal()

            # Guardar HTML en archivo temporal
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8')
            tmp.write(html)
            tmp.close()
            path = tmp.name.replace('\\', '/')
            file_url = f'file:///{path}'

            # Cargar en la pestaña
            pestana.url_var.set(file_url)
            pestana.cargar()
            self.notebook.tab(pestana.frame, text="Super Meme Finder")
            self.estado.config(text="MemeFinder abierto en nueva pestaña")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir MemeFinder: {e}")
            self.estado.config(text="Error al abrir MemeFinder")


    def cambiar_color_fondo(self, bg, fg):
        self.color_bg_actual = bg
        self.color_fg_actual = fg

        # para que cambie la barra del titulo de color tabien
        self.barra_titulo.config(bg=bg)
        if hasattr(self, "lbl_titulo"):
            self.lbl_titulo.config(bg=bg, fg=fg)

        self.frame_nav.config(bg=bg)
        # aplicar a todas las pestañas
        for pestana in self.pestanas:
            pestana.aplicar_color(bg, fg)


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
        self.grip = tk.Label(self.app, text="⠿", cursor="size_nw_se", bg="#FFFFFF", width=2)
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<Button-1>", self.grip_inicio)
        self.grip.bind("<B1-Motion>", self.grip_arrastrar)

    def grip_inicio(self, event):
        self.grip_x = event.x_root
        self.grip_y = event.y_root
        self.ancho_inicial = self.app.winfo_width()
        self.alto_inicial = self.app.winfo_height()

    def grip_arrastrar(self, event):
        ancho = self.ancho_inicial + (event.x_root - self.grip_x)
        alto = self.alto_inicial + (event.y_root - self.grip_y)
        ancho = max(400, ancho)
        alto = max(300, alto)
        self.app.geometry(f"{ancho}x{alto}")
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


    def abrir_link(self, url, nueva_pestana=False):
        if nueva_pestana:
            pestana = self.nueva_pestana()
            self.notebook.select(pestana.frame)
            self.app.update_idletasks()
        else:
            pestana = self.obtener_pestana_actual()
        if not pestana:
            return

        parsed = urlparse(url)
        if parsed.scheme == "search":
            termino = unquote(parsed.netloc + parsed.path)
            self.cargar_busqueda_en_pestana(termino, pestana)
            return

        if not parsed.scheme:
            current_url = pestana.obtener_url()
            if current_url.startswith("http"):
                url = urljoin(current_url, url)
            elif current_url.startswith("file:///"):
                ruta_base = os.path.dirname(current_url.replace("file:///", ""))
                ruta_rel = os.path.normpath(os.path.join(ruta_base, url))
                url = f"file:///{ruta_rel.replace('\\', '/') }"

        pestana.url_var.set(url)
        pestana.frame.update_idletasks()
        pestana.cargar()

    def cargar_busqueda_en_pestana(self, termino, pestana=None):
        motor = MotordeBusqueda()
        html = motor.obtener_resultados_busqueda(termino)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8')
        tmp.write(html)
        tmp.close()
        path = tmp.name.replace('\\', '/')
        file_url = f'file:///{path}'

        if pestana is None:
            pestana = self.obtener_pestana_actual()
        pestana.es_pagina_busqueda = True
        pestana.url_var.set(file_url)
        pestana.cargar()

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
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: (self.actualizar_menu_historial(), self.actualizar_menu_fav(), self.actualizar_estrella(), self.actualizar_botones_navegacion()))

        
        self.pestanas = []
        self.nueva_pestana()

    def actualizar_menu_historial(self):
        
        menus = [self.menu_historial]
        if hasattr(self, "menu_hist_principal"):
            menus.append(self.menu_hist_principal)

        for menu in menus:
            menu.delete(0, tk.END)
        
        #obbtener el historial de la pestaña activa
        pestana = self.pestana_actual()
        entradas = pestana.historial.obtener_historial()
        
        if not entradas:
            for menu in menus:
                menu.add_command(label="Historial vacio", state="disabled")
        else:
            for menu in menus:
                for url, titulo in reversed(entradas):
                    display_url = f"{url[:35]}..." if len(url) > 35 else url
                    menu.add_command(
                        label=f"{titulo} - {display_url}", command=lambda u=url: self.cargar_desde_historial(u))

    
    
    def recargar_pestana(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.recargar()

    def cargar_desde_historial(self, url):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        pestana.url_var.set(url)
        pestana.cargar()


    def cargar_archivo(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.cargar()


    def guardar_en_fav(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return

        url = pestana.obtener_url()
        if not url:
            self.estado.config(text="No hay URL para guardar")
            return

        tab_text = self.notebook.tab(self.notebook.select(), "text")
        titulo = tab_text if tab_text and tab_text != "Nueva pestaña" else pestana.obtener_nombre_archivo(url)

        if self.favoritos.contiene(url):
            self.favoritos.eliminar(url)
            self.btn_estrella_fav.config(text="☆")
            self.estado.config(text="Favorito eliminado")
        else:
            self.favoritos.agregar(url, titulo)
            self.btn_estrella_fav.config(text="★")
            self.estado.config(text="Agregado a favoritos ★")
        self.actualizar_estrella()
        self.actualizar_menu_fav()

    def actualizar_estrella(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        url = pestana.obtener_url()
        if self.favoritos.contiene(url):
            self.btn_estrella_fav.config(text="★")
        else:
            self.btn_estrella_fav.config(text="☆")


    def actualizar_menu_fav(self):
        # Limpiar el menú de favoritos
        menus = [self.menu_fav]
        if hasattr(self, "menu_fav_principal"):
            menus.append(self.menu_fav_principal)

        for menu in menus:
            menu.delete(0, tk.END)

        favoritos = self.favoritos.obtener_favoritos()

        if not favoritos:
            for menu in menus:
                menu.add_command(
                    label="No hay favoritos",
                    state="disabled"
                )
            return

        for url, titulo in favoritos:
            for menu in menus:
                menu.add_command(
                    label=url,
                    command=lambda u=url: self.cargar_desde_fav(u)
                )




    def cargar_desde_fav(self, url):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        pestana.url_var.set(url)
        pestana.cargar()
     
    def eliminar_favorito_actual(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        url = pestana.obtener_url()
        if not url:
            self.estado.config(text="No hay URL actual para eliminar")
            return
        self.favoritos.eliminar(url)
        self.actualizar_menu_fav()
        self.estado.config(text="Favorito eliminado")

    def nueva_pestana(self, titulo="Nueva pestaña"):
        
        pestana = Pestana(
            self.notebook,
            self.abrir_link,
            titulo=titulo,
            bg=self.color_bg_actual,
            fg=self.color_fg_actual,
            on_historial_update=self.actualizar_menu_historial,
            on_navegacion=self.actualizar_estrella,
            navegador=self
        )

        self.pestanas.append(pestana)
        return pestana

    def siguiente_pestana(self, event=None):
        total = len(self.pestanas)
        if total <=1:
            return
        actual = self.notebook.index(self.notebook.select())
        siguiente = (actual + 1)%total
        self.notebook.select(siguiente)

    def pestana_anterior(self, event=None):
        total = len(self.pestanas)
        if total <=1:
            return
        actual = self.notebook.index(self.notebook.select())
        anterior = (actual - 1)%total
        self.notebook.select(anterior)

    def ir_a_pestana(self, indice, event=None):
        if indice < len(self.pestanas):
            self.notebook.select(indice)   
    
    def obtener_pestana_actual(self):
        index = self.notebook.index(self.notebook.select())
        return self.pestanas[index]

    def pestana_actual(self):
        indice = self.notebook.index(self.notebook.select())
        return self.pestanas[indice]

    def cerrar_pestana_actual(self):
        indice_seleccion = self.notebook.index(self.notebook.select())
        indice_mas_reciente = len(self.pestanas) - 1
        # si hay solo una no se cierra
        if len(self.pestanas) <= 1:
            self.estado.config(text="No se puede cerrar")
            return
        
        if indice_seleccion == indice_mas_reciente:
            self.estado.config(text="No se puede cerrar la mas reciente")
            return
        
        pestana = self.pestanas.pop(indice_seleccion)
        pestana.cerrar()
        self.estado.config(text="Pestaña cerrada")

    def retroceder_pag(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.ir_atras()
            self.actualizar_botones_navegacion()

    def avanzar_pag(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.ir_adelante()
            self.actualizar_botones_navegacion()

    def actualizar_botones_navegacion(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            self.btn_atras.config(state="disabled")
            self.btn_adelante.config(state="disabled")
            return
        if pestana.historial_atras:
            self.btn_atras.config(state="normal")
        else:
            self.btn_atras.config(state="disabled")
        if pestana.historial_adelante:
            self.btn_adelante.config(state="normal")
        else:
            self.btn_adelante.config(state="disabled")

    def notificar_cambio_modo(self):
        if self.modo_offline.get():
            self.estado.config(text="Navegador en MODO OFFLINE", fg="red")
        else:
            self.estado.config(text="Navegador MODO ONLINE", fg="green")
        for pestana in self.pestanas:
            pestana.actualizar_estado_ia_por_offline()
        self.actualizar_botones_navegacion()