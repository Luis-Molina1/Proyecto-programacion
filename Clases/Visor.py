
import tkinter as tk
from html.parser import HTMLParser


class VisorHTML(HTMLParser):
    def __init__(self, text_widget, on_link_click=None):
        super().__init__()
        self.text_widget = text_widget
        self.on_link_click = on_link_click
        self.estilos_activos = []
        self.link_stack = []

        self.link_index = 0

        # Estilos de texto
        self.text_widget.tag_configure("h1", font=("Arial", 16, "bold"))
        self.text_widget.tag_configure("h2", font=("Arial", 14, "bold"))
        self.text_widget.tag_configure("b", font=("Arial", 12, "bold"))
        self.text_widget.tag_configure("i", font=("Arial", 12, "italic"))

        # Estilo de link
        self.text_widget.tag_configure("link",foreground="#0066cc",underline=True)
        self.text_widget.tag_configure("link_hover",foreground="#66b2ff",underline=True)


    # ---------- TAGS ----------

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "b", "i"):
            self.estilos_activos.append(tag)

        elif tag == "a":
            href = None
            for k, v in attrs:
                if k == "href":
                    href = v
                    break
            self.link_stack.append(href)

        elif tag in ("p", "br", "li"):
            self.text_widget.insert(tk.END, "\n")

    def handle_endtag(self, tag):
        if tag in self.estilos_activos:
            self.estilos_activos.remove(tag)

        elif tag == "a":
            self.link_stack.pop()
            self.text_widget.insert(tk.END, " ")

        elif tag in ("p", "li", "h1", "h2"):
            self.text_widget.insert(tk.END, "\n")

    # ---------- TEXTO ----------

    def handle_data(self, data):
        texto = data.strip()
        if not texto:
            return
        if self.link_stack and self.link_stack[-1]:
            self._insertar_link(texto, self.link_stack[-1])
        else:
            self.text_widget.insert(tk.END, texto + " ", self.estilos_activos)

    # ---------- LINK ----------

    def _insertar_link(self, texto, url):
        self.link_index += 1
        tag_link = f"link_{self.link_index}"

        # Insertar texto con el tag del link
        self.text_widget.insert(tk.END,texto,("link", tag_link))

        # Click
        if self.on_link_click:
            self.text_widget.tag_bind(tag_link,"<Button-1>",lambda e, u=url: self.on_link_click(u))

        # Hover: cambiar color
        self.text_widget.tag_bind(tag_link,"<Enter>",lambda e, t=tag_link: (self.text_widget.tag_configure(t, foreground="#66b2ff"),self.text_widget.config(cursor="hand2"))
        )
        # Salir: restaurar color
        self.text_widget.tag_bind(tag_link,"<Leave>",lambda e, t=tag_link: (self.text_widget.tag_configure(t, foreground="#0066cc"),self.text_widget.config(cursor=""))
        )

