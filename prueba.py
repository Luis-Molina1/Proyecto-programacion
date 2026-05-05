import tkinter as tk
from tkhtmlview import HTMLLabel

def main():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Visor HTML en Tkinter")
    root.geometry("500x400")

    # HTML de ejemplo (puede venir de un archivo o de internet)
    html_content = """
    <h1 style='color:blue;'>Hola desde HTML</h1>
    <p>Este es un <b>texto en negrita</b> y un <i>texto en cursiva</i>.</p>
    <ul>
        <li>Elemento 1</li>
        <li>Elemento 2</li>
    </ul>
    """

    # Crear widget HTMLLabel para mostrar el contenido
    html_label = HTMLLabel(root, html=html_content)
    html_label.pack(fill="both", expand=True, padx=10, pady=10)

    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Error: Debes instalar tkhtmlview con: pip install tkhtmlview")