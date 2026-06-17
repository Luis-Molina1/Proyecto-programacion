
import tkinter as tk
from html.parser import HTMLParser
from urllib.request import urlopen
import urllib.parse
from urllib.parse import urljoin

class VisorHTML(HTMLParser):
    def __init__(self, text_widget, on_link_click=None, pestana=None):
        super().__init__()
        
        self.text_widget = text_widget
        self.on_link_click = on_link_click
        self.pestana = pestana
        
        self.estilos_activos = []
        self.link_stack = []
        self.link_index = 0
        # guardar referencia de imagen
        self.imagenes_referencia = []
        self.tags_a_ignorar = []
        self.hr_frames = []
        self.list_stack = []
        self.in_button = False
        self.button_text = ""
        self.in_textarea = False
        self.textarea_text = ""
        self.textarea_attrs = {}
        self.container_stack = []
        self.center_frames = []
        self.current_container = None
        self.current_row_frame = None
        self.button_parent = None
        self.text_widget.bind("<Configure>", self._redimensionar_hrs, add="+")

        self.text_widget.tag_configure("h1", font=("Arial", 25, "bold"), spacing1=12, spacing3=6)
        self.text_widget.tag_configure("h2", font=("Arial", 20, "bold"), spacing1=10, spacing3=5)
        self.text_widget.tag_configure("h3", font=("Arial", 18, "bold"), spacing1=8, spacing3=4)
        self.text_widget.tag_configure("h4", font=("Arial", 15, "bold"), spacing1=8, spacing3=3)
        self.text_widget.tag_configure("h5", font=("Arial", 12, "bold"), spacing1=8, spacing3=2)
        self.text_widget.tag_configure("h6", font=("Arial", 10, "bold"), spacing1=8, spacing3=1)

        self.text_widget.tag_configure("i", font=("Arial", 12, "italic"))
        self.text_widget.tag_configure("em", font=("Arial", 12, "italic"))
        self.text_widget.tag_configure("p", font=("Arial", 12), spacing1=6, spacing3=6)
        self.text_widget.tag_configure("li", font=("Arial", 12), lmargin1=24, lmargin2=40, spacing1=3, spacing3=3)

        self.text_widget.tag_configure("b", font=("Arial", 20, "bold"))
        self.text_widget.tag_configure("strong", font=("Arial", 20, "bold"))
        self.text_widget.tag_configure("label", font=("Arial", 12))

        self.text_widget.tag_configure("link", foreground="#0066cc", underline=True)
        self.text_widget.tag_configure("link_hover", foreground="#66b2ff", underline=True)
        self.text_widget.tag_configure("center", justify="center")
        self.text_widget.tag_configure("right", justify="right")
        self.text_widget.tag_configure("error_tag", foreground="red", font=("Arial", 10, "bold"))
        self._input_by_id = {}
        self.align_stack = []

    def _registrar_input(self, input_id, widget, placeholder=""):
        self._input_by_id[input_id] = {
            "widget": widget,
            "placeholder": placeholder
        }

    def _limpiar_placeholder(self, entry):
        if hasattr(entry, "placeholder_text") and entry.get() == entry.placeholder_text:
            entry.delete(0, tk.END)

    def _crear_callback_desde_onclick(self, onclick):
        onclick = onclick.strip()
        if onclick.startswith("buscar"):
            return self._ejecutar_buscar
        return None

    def _ejecutar_buscar(self):
        if not self.on_link_click:
            return

        termino = ""
        if "campoBusqueda" in self._input_by_id:
            entry_widget = self._input_by_id["campoBusqueda"]["widget"]
            termino = entry_widget.get().strip()
            placeholder = self._input_by_id["campoBusqueda"]["placeholder"]
            if placeholder and termino == placeholder:
                termino = ""

        termino = termino.strip()
        if termino:
            termino_encoded = urllib.parse.quote(termino.lower())
            self.on_link_click(f"search://{termino_encoded}")

    def asegurar_nueva_linea(self):
        #evita insertar saltos de línea consecutivos
        ultimo = self.text_widget.get("end-2c", "end-1c")
        if ultimo and ultimo != "\n":
            self.text_widget.insert(tk.END, "\n")

    def _redimensionar_hrs(self, event=None):
        nuevo_ancho = self.text_widget.winfo_width()-5
        if nuevo_ancho > 0:
            for frame in self.hr_frames:
                try:
                    frame.config(width=nuevo_ancho)
                except tk.TclError:
                    pass
            for frame in self.center_frames:
                try:
                    frame.config(width=nuevo_ancho)
                except tk.TclError:
                    pass

    def handle_starttag(self, tag, attrs):
        etiquetas_reconocidas = [
            "script", "style", "head", "title", "ul", "ol", "h1", "h2", "h3", 
            "h4", "h5", "h6", "b", "strong", "i", "em", "p", "li", "label", 
            "a", "br", "hr", "input", "button", "img", "html", "body", "div", 
            "span", "meta", "link", "center", "section", "article", "footer",
            "header", "nav", "aside", "figure", "figcaption", "table", "tr", "th", "td",
            "form", "select", "option", "textarea", "audio", "video", "iframe", "canvas", "svg",
            "source", "track", "picture", "object", "embed"
        ]
        if tag not in etiquetas_reconocidas:
            self.text_widget.insert(tk.END, f"[Etiqueta no reconocida: {tag}] ", "error_tag")

        if tag in ("script", "style", "head", "title", "audio", "video", "iframe", "canvas", "svg", "picture", "object", "embed"):
            self.tags_a_ignorar.append(tag)
            if tag in ("audio", "video", "iframe", "canvas", "svg", "picture", "object", "embed"):
                self.asegurar_nueva_linea()
                if tag in ("video", "iframe", "canvas", "picture", "object", "embed"):
                    ancho = 300
                    alto = 150
                else:
                    ancho = 250
                    alto = 50
                texto_placeholder = f"[ {tag.capitalize()} ]"
                
                placeholder_frame = tk.Frame(self.text_widget, width=ancho, height=alto, bg="#e0e0e0", bd=1, relief="solid")
                placeholder_frame.pack_propagate(False)
                lbl = tk.Label(placeholder_frame, text=texto_placeholder, bg="#e0e0e0", fg="#555555", font=("Arial", 10, "italic"))
                lbl.pack(expand=True)
                
                self.text_widget.window_create(tk.END, window=placeholder_frame)
                self.asegurar_nueva_linea()
            return

        if tag == "center":
            self.asegurar_nueva_linea()
            center_frame = tk.Frame(self.text_widget)
            self.text_widget.window_create(tk.END, window=center_frame)
            self.text_widget.insert(tk.END, "\n")
            self.container_stack.append(center_frame)
            self.center_frames.append(center_frame)
            self.current_container = center_frame
            self.current_row_frame = None
            return

        if tag == "p" and self.current_container is not None:
            self.current_row_frame = tk.Frame(self.current_container)
            self.current_row_frame.pack(anchor="center", pady=5)
            return

        # block-level containers
        if tag in ("div", "section", "article", "header", "nav", "aside", "footer", "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol"):
            self.asegurar_nueva_linea()
            align = None
            dic_attrs = dict(attrs)
            align_val = dic_attrs.get("align", "").lower()
            if align_val in ("center", "right"):
                self.align_stack.append(align_val)
            if tag in ("ul", "ol"):
                self.list_stack.append({"type": tag, "count": 1})
                return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "b", "strong", "i", "em", "p", "li", "label"):
            self.estilos_activos.append(tag)
        

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li"):
            self.asegurar_nueva_linea()

        if tag == "li":
            prefijo = "  •  "
            if self.list_stack:
                lista_actual = self.list_stack[-1]
                if lista_actual["type"] == "ol":
                    prefijo = f"  {lista_actual['count']}.  "
                    lista_actual["count"] += 1
            self.text_widget.insert(tk.END, prefijo, self.estilos_activos)

        elif tag == "a":
            href = None
            target_blank = False
            for k, v in attrs:
                if k == "href":
                    href = v
                elif k == "target" and str(v).lower() == "_blank":
                    target_blank = True
            self.link_stack.append((href, target_blank))

        elif tag == "br":
            self.text_widget.insert(tk.END, "\n")

        elif tag == "hr":
            self.asegurar_nueva_linea()
            hr_frame = tk.Frame(self.text_widget, height=2, bg="gray", bd=1, relief="sunken")
            self.hr_frames.append(hr_frame)
            self.text_widget.window_create(tk.END, window=hr_frame)
            self.text_widget.insert(tk.END, "\n")
            
            self.text_widget.update_idletasks()
            ancho = self.text_widget.winfo_width() - 30
            if ancho > 0:
                hr_frame.config(width=ancho)

        elif tag == "input":
            dic_attrs = dict(attrs)
            tipo = dic_attrs.get("type", "text").lower()
            val = dic_attrs.get("value", "")
            placeholder = dic_attrs.get("placeholder", "")
            input_id = dic_attrs.get("id")
            if tipo in ("button", "submit", "reset"):
                texto_btn = val if val else "Button"
                parent = self.current_row_frame if self.current_row_frame is not None else self.text_widget
                btn = tk.Button(parent, text=texto_btn, font=("Arial", 12), cursor="hand2")
                if parent == self.text_widget:
                    self.text_widget.window_create(tk.END, window=btn)
                else:
                    btn.pack(side="left", padx=5, pady=5)
            else:
                entry = tk.Entry(self.current_row_frame if self.current_row_frame is not None else self.text_widget, font=("Arial", 12), width=40)
                if val:
                    entry.insert(0, val)
                elif placeholder:
                    entry.insert(0, placeholder)
                    entry.placeholder_text = placeholder
                    entry.bind("<FocusIn>", lambda e, ent=entry: self._limpiar_placeholder(ent))
                if input_id:
                    self._registrar_input(input_id, entry, placeholder)
                if self.current_row_frame is not None:
                    entry.pack(side="left", padx=5, pady=5)
                else:
                    self.text_widget.window_create(tk.END, window=entry)
            if self.current_row_frame is None:
                self.text_widget.insert(tk.END, " ")

        elif tag == "button":
            if self.current_container is not None and self.current_row_frame is not None:
                self.in_button = True
                self.button_text = ""
                self.button_onclick = None
                self.button_parent = self.current_row_frame
                for k, v in attrs:
                    if k.lower() == "onclick":
                        self.button_onclick = v
            else:
                self.in_button = True
                self.button_text = ""
                self.button_onclick = None
                self.button_parent = None
                for k, v in attrs:
                    if k.lower() == "onclick":
                        self.button_onclick = v

        elif tag == "textarea":
            self.in_textarea = True
            self.textarea_text = ""
            self.textarea_attrs = dict(attrs)

        elif tag == "img":
            dic_attrs = dict(attrs)
            src = dic_attrs.get("src")
            if src:
                self._insertar_imagen(src)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head", "title", "audio", "video", "iframe", "canvas", "svg", "picture", "object", "embed"):
            if tag in self.tags_a_ignorar:
                self.tags_a_ignorar.remove(tag)
            return

        if tag == "center":
            if self.container_stack:
                self.container_stack.pop()
            self.current_container = self.container_stack[-1] if self.container_stack else None
            self.current_row_frame = None
            self.asegurar_nueva_linea()
            return

        if tag == "p" and self.current_container is not None:
            self.current_row_frame = None
            self.asegurar_nueva_linea()
            return

        if tag in self.estilos_activos:
            self.estilos_activos.remove(tag)

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li"):
            self.asegurar_nueva_linea()

        elif tag == "a":
            if self.link_stack:
                self.link_stack.pop()
            self.text_widget.insert(tk.END, " ")

        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.asegurar_nueva_linea()

        elif tag in ("div", "section", "article", "header", "nav", "aside", "footer"):
            self.asegurar_nueva_linea()

        elif tag == "button":
            if self.in_button:
                self.in_button = False
                texto_btn = self.button_text.strip()
                if not texto_btn:
                    texto_btn = "Button"
                parent = getattr(self, "button_parent", None)
                if parent is None:
                    parent = self.text_widget
                btn = tk.Button(parent, text=texto_btn, font=("Arial", 12), cursor="hand2")
                if getattr(self, "button_onclick", None):
                    callback = self._crear_callback_desde_onclick(self.button_onclick)
                    if callback:
                        btn.config(command=callback)
                if parent == self.text_widget:
                    self.text_widget.window_create(tk.END, window=btn)
                    self.text_widget.insert(tk.END, " ")
                else:
                    btn.pack(side="left", padx=5, pady=5)
                self.button_onclick = None
                self.button_parent = None

        elif tag == "textarea":
            if self.in_textarea:
                self.in_textarea = False
                texto_ta = self.textarea_text
                rows = int(self.textarea_attrs.get("rows", 4))
                cols = int(self.textarea_attrs.get("cols", 40))
                
                ta_widget = tk.Text(self.text_widget, width=cols, height=rows, font=("Arial", 12), bd=1, relief="solid")
                if texto_ta:
                    ta_widget.insert(tk.END, texto_ta)
                
                self.text_widget.window_create(tk.END, window=ta_widget)
                self.text_widget.insert(tk.END, " ")

    def handle_data(self, data):
        if self.tags_a_ignorar:
            return
            
        if self.in_button:
            self.button_text += data
            return

        if self.in_textarea:
            self.textarea_text += data
            return
            
        texto = data.strip()
        if not texto:
            return
        if self.link_stack and self.link_stack[-1] and self.link_stack[-1][0]:
            url, target_blank = self.link_stack[-1]
            self._insertar_link(texto, url, target_blank)
        else:
            if self.current_container is not None and self.estilos_activos:
                style = self.estilos_activos[-1]
                if style in ("h1", "h2", "h3", "h4", "h5", "h6", "p"):
                    parent = self.current_row_frame if self.current_row_frame is not None else self.current_container
                    font_map = {
                        "h1": ("Arial", 25, "bold"),
                        "h2": ("Arial", 20, "bold"),
                        "h3": ("Arial", 18, "bold"),
                        "h4": ("Arial", 15, "bold"),
                        "h5": ("Arial", 12, "bold"),
                        "h6": ("Arial", 10, "bold")
                    }
                    font = font_map.get(style, ("Arial", 12))
                    label = tk.Label(parent, text=texto, font=font, justify="center")
                    label.pack()
                    return
            tags = self.estilos_activos.copy()
            if self.align_stack:
                align_tag = self.align_stack[-1]
                if align_tag in ("center", "right"):
                    tags.append(align_tag)
            self.text_widget.insert(tk.END, texto + " ", tags)

    def _insertar_link(self, texto, url, target_blank=False):
        self.link_index += 1
        tag_link = f"link_{self.link_index}"

        # insertar texto con el tag del link
        self.text_widget.insert(tk.END,texto,("link", tag_link))

        # Solo forzar nuevas pestañas para páginas de resultados de búsqueda
        # y para enlaces explícitamente marcados con target="_blank".
        abrir_en_nueva_pestana = target_blank
        if not abrir_en_nueva_pestana and getattr(self.pestana, "es_pagina_busqueda", False):
            abrir_en_nueva_pestana = url.startswith(("http://", "https://"))
        elif not abrir_en_nueva_pestana:
            abrir_en_nueva_pestana = False

        # Click
        if self.on_link_click:
            self.text_widget.tag_bind(
                tag_link,
                "<Button-1>",
                lambda e, u=url, abrir_en_nueva_pestana=abrir_en_nueva_pestana: self.on_link_click(u, nueva_pestana=abrir_en_nueva_pestana)
            )

        self.text_widget.tag_bind(tag_link,"<Enter>",lambda e, t=tag_link: (self.text_widget.tag_configure(t, foreground="#66b2ff"),self.text_widget.config(cursor="hand2"))
        )
        self.text_widget.tag_bind(tag_link,"<Leave>",lambda e, t=tag_link: (self.text_widget.tag_configure(t, foreground="#0066cc"),self.text_widget.config(cursor=""))
        )

    def _insertar_imagen(self, url_img):
        try:
            # indicar en la barra de estado que se está cargando una imagen
            if self.pestana and hasattr(self.pestana, "estado_var"):
                try:
                    self.pestana.estado_var.set("Cargando imagen...")
                except Exception:
                    pass

            if self.pestana:
                url_base = self.pestana.url_var.get().strip()
            else:
                url_base = ""
            url_completa = urljoin(url_base, url_img)
            parsed = urllib.parse.urlparse(url_completa)

            if parsed.scheme in ("http", "https"):
                with urlopen(url_completa) as response:
                    raw_data = response.read()
                tk_img = tk.PhotoImage(data=raw_data)
            else:
                ruta_limpia = url_img.replace("file:///", "")
                tk_img = tk.PhotoImage(file=ruta_limpia)

            self.imagenes_referencia.append(tk_img)
            self.text_widget.image_create(tk.END, image=tk_img)
            self.text_widget.insert(tk.END, "\n")

            # indicar finalización
            if self.pestana and hasattr(self.pestana, "estado_var"):
                try:
                    self.pestana.estado_var.set("Completado")
                except Exception:
                    pass

        except Exception as e:
            print(f"Error al cargar imagen {url_img}: {e}")
            self.text_widget.insert(tk.END, f"[Error al cargar imagen: {url_img}]\n")
    
    def reset(self):
        super().reset()
        self.imagenes_referencia = []
        self.tags_a_ignorar = []
        self.hr_frames = []
        self.list_stack = []
        self.in_button = False
        self.button_text = ""
        self.container_stack = []
        self.center_frames = []
        self.current_container = None
        self.current_row_frame = None
        self._input_by_id = {}
        self.align_stack = []
        self.in_textarea = False
        self.textarea_text = ""
        self.textarea_attrs = {}