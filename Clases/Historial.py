class Historial:
    def __init__(self):
        self.entradas = []
        self.limite = 10
    def agregar(self, url, titulo):
        if self.entradas and self.entradas[-1][0] == url:
            return
        self.entradas.append((url, titulo))
        if len(self.entradas) > self.limite:
            self.entradas.pop(0)
    def obtener_historial(self):
        return self.entradas
    