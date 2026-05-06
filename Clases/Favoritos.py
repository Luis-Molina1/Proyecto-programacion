class Favoritos:
    def __init__(self):
        self.lista = []
    def agregar(self, url, titulo):
        if not any(f[0] == url for f in self.lista):
            self.lista.append((url,titulo))
            return True
        return False
    def eliminar(self,url):
        self.lista= [f for f in self.lista if f[0]!= url]
    def obtener_favoritos(self):
        return self.lista
    