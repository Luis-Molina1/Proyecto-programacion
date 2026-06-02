
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

        self.text_widget.tag_configure("h1", font=("Arial", 18, "bold"), spacing1=12, spacing3=6)
        self.text_widget.tag_configure("h2", font=("Arial", 15, "bold"), spacing1=10, spacing3=5)
        self.text_widget.tag_configure("h3", font=("Arial", 13, "bold"), spacing1=8, spacing3=4)
        self.text_widget.tag_configure("b", font=("Arial", 12, "bold"))
        self.text_widget.tag_configure("i", font=("Arial", 12, "italic"))
        self.text_widget.tag_configure("p", font=("Arial", 12), spacing1=6, spacing3=6)
        self.text_widget.tag_configure("li", font=("Arial", 12), lmargin1=24, lmargin2=40, spacing1=3, spacing3=3)

        self.text_widget.tag_configure("link", foreground="#0066cc", underline=True)
        self.text_widget.tag_configure("link_hover", foreground="#66b2ff", underline=True)

    def asegurar_nueva_linea(self):
        #evita insertar saltos de línea consecutivos
        ultimo = self.text_widget.get("end-2c", "end-1c")
        if ultimo and ultimo != "\n":
            self.text_widget.insert(tk.END, "\n")

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "b", "i", "p", "li"):
            self.estilos_activos.append(tag)

        if tag in ("h1", "h2", "h3", "p", "li"):
            self.asegurar_nueva_linea()

        if tag == "li":
            self.text_widget.insert(tk.END, "  •  ", self.estilos_activos)

        elif tag == "a":
            href = None
            for k, v in attrs:
                if k == "href":
                    href = v
                    break
            self.link_stack.append(href)

        elif tag == "br":
            self.text_widget.insert(tk.END, "\n")

        elif tag == "img":
            dic_attrs = dict(attrs)
            src = dic_attrs.get("src")
            if src:
                self._insertar_imagen(src)

    def handle_endtag(self, tag):
        if tag in self.estilos_activos:
            self.estilos_activos.remove(tag)

        if tag in ("h1", "h2", "h3", "p", "li"):
            self.asegurar_nueva_linea()

        elif tag == "a":
            if self.link_stack:
                self.link_stack.pop()
            self.text_widget.insert(tk.END, " ")

    def handle_data(self, data):
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