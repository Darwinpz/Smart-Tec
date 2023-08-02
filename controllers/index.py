from flask import render_template, session, redirect, url_for, request,jsonify
from database.mongodb import MongoDb
import controllers.ctl_history as hist
from bson.objectid import ObjectId
from controllers.validaciones import Validaciones as val
import controllers.encrypt as encrypt
import os
import uuid
#import qrcode
db = MongoDb().db()


def cerrar_sesion():
    if val.validar_session(session):
        hist.guardar_historial(
            "CORRECTO", "SALIR", 'CIERRE DE SESIÓN CON ÉXITO - CÉDULA: "'+session["cedula"]+'"')
        session.pop('ip', None)
        session.pop('id', None)
        session.pop('cedula', None)
        session.pop('nombre', None)
        session.pop('rol', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('err_403'))
    
def index(request):

    alerts = {"tipo": "", "message": ""}

    try:

        if request.method == 'GET':
            if val.validar_session(session):
                return redirect(url_for("principal"))
            else:
                return render_template('/views/index.html')
        else:

            nom_usuario = val.val_vacio("usuario","",request)
            clave = val.val_vacio("clave","",request)

            if nom_usuario == os.getenv("USER_ADMIN") and clave == os.getenv("PWD_ADMIN"):
                session["ip"] = request.environ['REMOTE_ADDR']
                session["id"] = ObjectId().__str__()
                session["cedula"] = "0000000000"
                session["nombre"] = "SUPER-ADMIN"
                session["rol"] = "Super-Admin"

                hist.guardar_historial(
                    "CORRECTO", "INGRESO", 'INGRESO CON ÉXITO AL SISTEMA - SUPER-ADMIN: "'+session["cedula"]+'"')

                return redirect(url_for("principal"))

            usuario = list(db.usuarios.aggregate([
                {"$lookup": {"from": "servidores", "localField": "cedula",
                             "foreignField": "cedula", "as": "servidor"}},
                {"$unwind": "$servidor"},
                {"$project": {"servidor._id": 0}},
                {"$match": {"$or": [{"servidor.cedula": nom_usuario}, {"usuario": nom_usuario}, {
                    "servidor.correo": nom_usuario}]}},
            ]))

            if len(usuario) > 0:

                usuario = usuario[0]

                if clave == encrypt.decrypt(usuario["clave"]):

                    if usuario["estado"] == "ACTIVO":
                        session["ip"] = request.environ['REMOTE_ADDR']
                        session["id"] = str(usuario["_id"])
                        session["cedula"] = usuario["servidor"]["cedula"]
                        session["nombre"] = usuario["servidor"]["nombres"]
                        session["rol"] = usuario["rol"]

                        hist.guardar_historial(
                            "CORRECTO", "INGRESO", 'INGRESO CON ÉXITO AL SISTEMA - CÉDULA: "'+session["cedula"]+'"')

                        return redirect(url_for("principal"))
                    else:
                        alerts["tipo"] = "danger"
                        alerts["message"] = "Usuario Inactivo o No existe"
                        return render_template('/views/index.html', alert=alerts)
                else:
                    alerts["tipo"] = "danger"
                    alerts["message"] = "Clave incorrecta"
                    return render_template('/views/index.html', alert=alerts)
            else:
                alerts["tipo"] = "danger"
                alerts["message"] = "Usuario incorrecto"
                return render_template('/views/index.html', alert=alerts)
    except Exception as e:
        alerts["tipo"] = "danger"
        alerts["message"] = str(e)
        hist.guardar_historial(
            "ERROR", "INGRESO", 'ERROR DE INGRESO AL SISTEMA - "'+str(e)+'"')
        return redirect(url_for('err_500'))

def principal():
    if val.validar_session(session):
        return render_template('/views/principal.html', session=session)
    else:
        return redirect(url_for('index'))


#def ticket():
    try:

        if request.method == 'POST':
            
            foto = request.files['foto']
                
            if foto.filename != '':

                path_placa = ("static/placas")
                path_qr = ("static/qr")

                val.crear_directorio(os, path_placa)
                val.crear_directorio(os, path_qr)

                id = str(uuid.uuid1())
                file_ext = os.path.splitext(foto.filename)[1]
                url_foto = id+file_ext
                foto.save(os.path.join(path_placa, url_foto))

                qr = qrcode.QRCode(version=1,box_size=10,border=5)
                qr.add_data("ID: "+id+"\n Fecha de Ingreso: ")
                qr.make(fit=True)

                img = qr.make_image(fill="black",back_color="white")
                img.save(os.path.join(path_qr, id+".png"))

            else:
                return jsonify({"message": "Imagen no encontrada"}), 404
        else:
            return jsonify({"message": "Petición Incorrecta"}), 500

    except Exception as e:
            hist.guardar_historial(
                "ERROR", "INGRESO", 'ERROR AL GENERAR CÓDIGO QR - "'+str(e)+'"')
            return redirect(url_for('err_500'))
