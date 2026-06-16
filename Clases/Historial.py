class Historial:
    def __init__(self):
        self.entradas = []
        self.limite = 10
    def agregar(self, url, titulo):
        self.entradas= [entrada for entrada in self.entradas if entrada[0] != url]
        self.entradas.append((url, titulo))
        if len(self.entradas) > self.limite:
            self.entradas.pop(0)
    def obtener_historial(self):
        return self.entradas
    