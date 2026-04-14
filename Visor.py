import tkinter as tk
from html.parser import HTMLParser

class VisorHTML(HTMLParser):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.etiquetas_activas = []
        
        self.text_widget.tag_configure("h1", font=("Arial", 16, "bold"))
        self.text_widget.tag_configure("h2", font=("Arial", 14, "bold"))
        self.text_widget.tag_configure("b", font=("Arial", 12, "bold"))
        self.text_widget.tag_configure("i", font=("Arial", 12, "italic"))

    def handle_starttag(self, tag, attrs):
        self.etiquetas_activas.append(tag)
        if tag in ['p', 'h1', 'h2', 'br', 'li']:
            self.text_widget.insert(tk.END, "\n")

    def handle_endtag(self, tag):
        if tag in self.etiquetas_activas:
            self.etiquetas_activas.remove(tag)
        if tag in ['p', 'h1', 'h2', 'li']:
            self.text_widget.insert(tk.END, "\n")

    def handle_data(self, data):
        texto = data.strip()
        if not texto:
            return
        estilos_a_aplicar = [t for t in self.etiquetas_activas if t in ["h1", "h2", "b", "i"]]