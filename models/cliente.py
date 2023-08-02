from datetime import datetime

class Cliente:
    
    def __init__(self, cedula, nombres, correo, placa, url_foto):
        self.cedula = cedula
        self.nombres = nombres
        self.correo = correo
        self.placa = placa
        self.url_foto = url_foto

    def obtener_cliente(self):
        return self.__dict__
    
    def crear_cliente(self):
        self.fecha_creacion = datetime.now()
    
    def update_cliente(self):
        self.fecha_modificacion = datetime.now()
    