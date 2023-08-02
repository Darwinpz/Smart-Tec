from datetime import datetime

class Sensor:
    
    def __init__(self, piso, seccion, plaza, nombre, estado):
        self.piso = piso
        self.seccion = seccion
        self.plaza = plaza
        self.nombre = nombre
        self.estado = estado

    def obtener_sensor(self):
        return self.__dict__
    
    def crear_sensor(self):
        self.fecha_creacion = datetime.now()
    
    def update_sensor(self):
        self.fecha_modificacion = datetime.now()