from datetime import datetime

class Cobranza:
    
    def __init__(self, placa, ingreso, salida, total):
        self.placa = placa
        self.ingreso = ingreso
        self.salida = salida
        self.total = total

    def obtener_cobranza(self):
        return self.__dict__
    
    def crear_cobranza(self):
        self.fecha_creacion = datetime.now()
    
    def update_cobranza(self):
        self.fecha_modificacion = datetime.now()
    