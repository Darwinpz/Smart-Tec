from datetime import datetime

class Cliente:
    
    def __init__(self, cedula,clave, nombres, correo, placa):
        self.cedula = cedula
        self.clave = clave
        self.nombres = nombres
        self.correo = correo
        self.placa = placa

    def obtener_cliente(self):
        return self.__dict__
    
    def crear_cliente(self):
        self.fecha_creacion = datetime.now()
    
    def update_cliente(self):
        self.fecha_modificacion = datetime.now()
    