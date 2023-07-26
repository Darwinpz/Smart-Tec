from datetime import datetime

class Servidor:
    
    def __init__(self, cedula, nombres, correo, estado, url_foto):
        self.cedula = cedula
        self.nombres = nombres
        self.correo = correo
        self.estado = estado
        self.url_foto = url_foto

    def obtener_servidor(self):
        return self.__dict__
    
    def crear_servidor(self):
        self.fecha_creacion = datetime.now()
    
    def update_servidor(self):
        self.fecha_modificacion = datetime.now()
    