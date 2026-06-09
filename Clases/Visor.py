
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
        self.text_widget.tag_configure("error_tag", foreground="red", font=("Arial", 10, "bold"))

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

    def handle_starttag(self, tag, attrs):
        etiquetas_reconocidas = [
            "script", "style", "head", "title", "ul", "ol", "h1", "h2", "h3", 
            "h4", "h5", "h6", "b", "strong", "i", "em", "p", "li", "label", 
            "a", "br", "hr", "input", "button", "img", "html", "body", "div", 
            "span", "meta", "link", "center", "div", "section", "article", "span", "footer",
            "header", "nav", "aside", "figure"
        ]
        if tag not in etiquetas_reconocidas:
            self.text_widget.insert(tk.END, f"[Etiqueta no reconocida: {tag}] ", "error_tag")

        if tag in ("script", "style", "head", "title"):
            self.tags_a_ignorar.append(tag)
            return

        if tag in ("ul", "ol"):
            self.list_stack.append({"type": tag, "count": 1})
            self.asegurar_nueva_linea()
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
            for k, v in attrs:
                if k == "href":
                    href = v
                    break
            self.link_stack.append(href)

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
            if tipo in ("button", "submit", "reset"):
                texto_btn = val if val else "Button"
                btn = tk.Button(self.text_widget, text=texto_btn, font=("Arial", 12), cursor="hand2")
                self.text_widget.window_create(tk.END, window=btn)
            else:
                entry = tk.Entry(self.text_widget, font=("Arial", 12))
                if val:
                    entry.insert(0, val)
                elif placeholder:
                    entry.insert(0, placeholder)
                self.text_widget.window_create(tk.END, window=entry)
            self.text_widget.insert(tk.END, " ")

        elif tag == "button":
            self.in_button = True
            self.button_text = ""

        elif tag == "img":
            dic_attrs = dict(attrs)
            src = dic_attrs.get("src")
            if src:
                self._insertar_imagen(src)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head", "title"):
            if tag in self.tags_a_ignorar:
                self.tags_a_ignorar.remove(tag)
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

        elif tag == "button":
            if self.in_button:
                self.in_button = False
                texto_btn = self.button_text.strip()
                if not texto_btn:
                    texto_btn = "Button"
                btn = tk.Button(self.text_widget, text=texto_btn, font=("Arial", 12), cursor="hand2")
                self.text_widget.window_create(tk.END, window=btn)
                self.text_widget.insert(tk.END, " ")

    def handle_data(self, data):
        if self.tags_a_ignorar:
            return
            
        if self.in_button:
            self.button_text += data
            return
            
        texto = data.strip()
        if not texto:
            return
        if self.link_stack and self.link_stack[-1]:
            self._insertar_link(texto, self.link_stack[-1])
        else:
            self.text_widget.insert(tk.END, texto + " ", self.estilos_activos)

    def _insertar_link(self, texto, url):
        self.link_index += 1
        tag_link = f"link_{self.link_index}"

        # insertar texto con el tag del link
        self.text_widget.insert(tk.END,texto,("link", tag_link))

        # Click
        if self.on_link_click:
            self.text_widget.tag_bind(tag_link,"<Button-1>",lambda e, u=url: self.on_link_click(u))

        self.text_widget.tag_bind(tag_link,"<Enter>",lambda e, t=tag_link: (self.text_widget.tag_configure(t, foreground="#66b2ff"),self.text_widget.config(cursor="hand2"))
        )
        self.text_widget.tag_bind(tag_link,"<Leave>",lambda e, t=tag_link: (self.text_widget.tag_configure(t, foreground="#0066cc"),self.text_widget.config(cursor=""))
        )

    def _insertar_imagen(self, url_img):
        try:
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