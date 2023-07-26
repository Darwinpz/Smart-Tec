class Validaciones:

    def validar_session(session):
        if 'id' in session:
            return True
        
    def val_vacio(nombre,defecto,request):
        return request.form[nombre] if (nombre in request.form) else defecto
    
    def crear_directorio(os,path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def del_archivo(os, path):
        if os.path.exists(path):
            os.remove(path)