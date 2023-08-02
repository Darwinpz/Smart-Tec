from datetime import datetime

class Piso:
    
    def __init__(self, nombre, items):
        self.nombre = nombre
        self.items = items

    def obtener_piso(self):
        return self.__dict__
    
    def crear_piso(self):
        self.fecha_creacion = datetime.now()
    
    def update_piso(self):
        self.fecha_modificacion = datetime.now()
    