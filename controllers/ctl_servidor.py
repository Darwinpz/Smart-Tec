from flask import jsonify, session
from database.mongodb import MongoDb
import controllers.ctl_history as hist
from controllers.validaciones import Validaciones as val
from models.servidor import Servidor
from bson.objectid import ObjectId
import uuid
import json
import os

db = MongoDb().db()

def save_servidores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                foto = request.files['s_foto']
                cedula = val.val_vacio("s_cedula", "", request).upper().strip()
                ciudadano = val.val_vacio(
                    "s_ciudadano", "", request).upper().strip()
                correo = val.val_vacio("s_correo", "", request).lower().strip()
                estado = val.val_vacio("s_estado", "", request).upper().strip()

                path = ("static/servidores")

                val.crear_directorio(os, path)

                url_foto = ""

                if cedula != "" and ciudadano != "" and correo != "" and estado != "":

                    existe = db.servidores.find_one(
                        {"$or": [{'cedula': cedula}, {'correo': correo}]})

                    if existe:
                        return jsonify({"message": "Cedula y/o Correo de Servidor Existente"}), 404
                    else:

                        if foto.filename != '':
                            id = str(uuid.uuid1())
                            file_ext = os.path.splitext(foto.filename)[1]
                            url_foto = id+file_ext
                            foto.save(os.path.join(path, url_foto))

                        servidor = Servidor(cedula, ciudadano, correo, estado, url_foto)
                        servidor.crear_servidor()
                        _id = db.servidores.insert_one(
                            servidor.obtener_servidor()).inserted_id
                        hist.guardar_historial(
                            "CORRECTO", "CREAR", 'SERVIDOR "'+cedula+'" CON ID "'+str(_id)+'" CREADO CORRECTAMENTE')
                        return jsonify({"message": "Servidor Creado Correctamente"}), 200
                else:
                    return jsonify({"message": "Información Incompleta"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "CREAR", 'ERROR AL CREAR EL SERVIDOR "'+cedula+'" - "'+str(e)+'"')
            val.del_archivo(os, os.path.join(path, url_foto))
            return jsonify({"message": "Error al Crear el servidor"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def ver_servidores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                validar = val.val_vacio("s_validar", "", request).strip()

                servidores = []

                if validar == "":

                    servidores = db.servidores.aggregate([

                        {"$match": {'cedula': {
                            "$nin":  [session["cedula"]]}}}
                    ])
                else:

                    datos = list(db.servidores.find(
                        {}, {"_id": 1, "cedula": 1, "nombres": 1}))

                    for s in datos:
                        if db.usuarios.find_one({"cedula": s["cedula"]}) == None:
                            servidores.append(s)

                data = {"data": list(servidores)}

                return json.dumps(data, default=str), 200
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "VISUALIZAR", 'ERROR AL VISUALIZAR TODOS LOS SERVIDORES - "'+str(e)+'"')
            return jsonify({"message": "Error al Visualizar todos los servidores"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def edit_servidores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                foto = request.files['s_foto']
                cedula = val.val_vacio("s_cedula", "", request).upper().strip()
                ciudadano = val.val_vacio(
                    "s_ciudadano", "", request).upper().strip()
                correo = val.val_vacio("s_correo", "", request).lower().strip()
                estado = val.val_vacio("s_estado", "", request).upper().strip()

                if cedula != "" and ciudadano != "" and correo != "" and estado != "":

                    existe = db.servidores.find_one(
                        {"$or": [{'cedula': cedula}, {'correo': correo}]})

                    if existe:

                        path = ("static/servidores")

                        val.crear_directorio(os, path)

                        url_foto = existe["url_foto"]

                        if foto.filename != '':

                            if existe["url_foto"] != "":
                                path_temp = (
                                    "static/servidores/"+existe["url_foto"])
                                val.del_archivo(os, path_temp)

                            id = str(uuid.uuid1())
                            file_ext = os.path.splitext(foto.filename)[1]
                            url_foto = id+file_ext
                            foto.save(os.path.join(path, url_foto))

                        servidor = Servidor(cedula, ciudadano, correo, estado, url_foto)
                        servidor.update_servidor()
                        db.servidores.update_one({"_id": ObjectId(existe["_id"])}, {
                            "$set": servidor.obtener_servidor()})
                        hist.guardar_historial(
                            "CORRECTO", "ACTUALIZAR", 'SERVIDOR "'+cedula+'" CON ID "'+str(existe["_id"])+'" ACTUALIZADO CORRECTAMENTE')
                        return jsonify({"message": "Servidor Actualizado Correctamente"}), 200
                    else:
                        return jsonify({"message": "Servidor No Existente"}), 404
                else:
                    return jsonify({"message": "Información Incompleta"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ACTUALIZAR", 'ERROR AL ACTUALIZAR EL SERVIDOR "'+cedula+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Actualizar el servidor"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def del_servidores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                cedula = val.val_vacio("cedula", "", request).upper().strip()
                existe = db.servidores.find_one({"cedula": cedula})

                if existe:

                    ver_usuario = db.usuarios.find_one({"cedula": cedula})

                    if ver_usuario:
                        return jsonify({"message": "Debes eliminar el USUARIO asignado"}), 404
                    else:

                        if existe["url_foto"] != "":
                            path = ("static/servidores/"+existe["url_foto"])
                            val.del_archivo(os, path)
                        db.servidores.delete_one({"cedula": cedula})
                        hist.guardar_historial(
                            "CORRECTO", "ELIMINAR", 'SERVIDOR "'+cedula+'" ELIMINADO CORRECTAMENTE')
                    return jsonify({"message": "Servidor Eliminado Correctamente"}), 200
                else:
                    return jsonify({"message": "Servidor NO Existente"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ELIMINAR", 'ERROR AL ELIMINAR EL SERVIDOR "'+cedula+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Eliminar el servidor"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500
