from flask import jsonify, session
from database.mongodb import MongoDb
import controllers.ctl_history as hist
from controllers.validaciones import Validaciones as val
from models.piso import Piso
from bson.objectid import ObjectId
import json

db = MongoDb().db()

def save_pisos(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                nombre = val.val_vacio("p_nombre", "", request).upper().strip()

                item_seccion = request.form.getlist("seccion[]")
                item_plaza = request.form.getlist("plaza[]")
                
                if  nombre != "":

                    existe = db.pisos.find_one(
                        {"$or": [{'nombre': nombre}]})

                    if existe:
                        return jsonify({"message": "Piso Existente"}), 404
                    else:

                        items = []

                        if len(item_seccion) == len(item_plaza):
                            for i in range(len(item_seccion)):
                                items.append(
                                    {"seccion": item_seccion[i], "plaza": int(item_plaza[i])})

                        piso = Piso(nombre, items)
                        piso.crear_piso()
                        _id = db.pisos.insert_one(
                            piso.obtener_piso()).inserted_id
                        hist.guardar_historial(
                            "CORRECTO", "CREAR", 'PISO "'+nombre+'" CON ID "'+str(_id)+'" CREADO CORRECTAMENTE')
                        return jsonify({"message": "Piso Creado Correctamente"}), 200
                else:
                    return jsonify({"message": "Información Incompleta"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "CREAR", 'ERROR AL CREAR EL PISO "'+nombre+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Crear el piso"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def ver_pisos(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                pisos =db.pisos.aggregate([
                        {"$addFields": {
                            "count_seccion":{"$size": "$items"},
                            "count_plaza": {"$sum": "$items.plaza"}
                        }}
                ])
                
                data = {"data": list(pisos)}

                return json.dumps(data, default=str), 200
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "VISUALIZAR", 'ERROR AL VISUALIZAR TODOS LOS PISOS - "'+str(e)+'"')
            return jsonify({"message": "Error al Visualizar todos los pisos"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def edit_pisos(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                nombre = val.val_vacio("p_nombre", "", request).upper().strip()
                item_seccion = request.form.getlist("seccion[]")
                item_plaza = request.form.getlist("plaza[]")

                id = val.val_vacio("p_codigo", "", request).strip()

                existe = db.pisos.find_one({"_id": ObjectId(id)})

                if existe:

                    existe_nombre = db.pisos.find_one(
                        {"nombre": nombre})

                    if existe_nombre:
                        if existe_nombre["_id"] != existe["_id"]:
                            return jsonify({"message": "No se puede actualizar, piso Existente"}), 404

                    items = []

                    if len(item_seccion) == len(item_plaza):
                        for i in range(len(item_seccion)):
                            items.append({"seccion": item_seccion[i], "plaza": int(item_plaza[i])})

                    piso = Piso(nombre, items)
                    piso.update_piso()
                    db.pisos.update_one({"_id": ObjectId(id)}, {
                        "$set": piso.obtener_piso()})
                    hist.guardar_historial(
                        "CORRECTO", "ACTUALIZAR", 'PISO "'+nombre + '" CON ID "'+str(id)+'" ACTUALIZADO CORRECTAMENTE')
                    return jsonify({"message": "Piso Actualizado Correctamente"}), 200
                else:
                    return jsonify({"message": "Piso No existe"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ACTUALIZAR", 'ERROR AL ACTUALIZAR EL PISOS "'+nombre+'" CON ID "'+str(id)+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Actualizar el Piso"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def del_pisos(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                id = val.val_vacio("id", "", request).strip()
                nombre = val.val_vacio("p_nombre", "", request).upper().strip()
                existe = db.pisos.find_one({"_id": ObjectId(id)})

                if existe:

                    db.pisos.delete_one({"_id": ObjectId(id)})
                    hist.guardar_historial(
                            "CORRECTO", "ELIMINAR", 'PISO "'+nombre+'" CON ID "'+str(id)+'" ELIMINADO CORRECTAMENTE')
                    return jsonify({"message": "Piso Eliminado Correctamente"}), 200
                        
                else:
                    return jsonify({"message": "Piso NO Existente"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ELIMINAR", 'ERROR AL ELIMINAR EL PISO "'+nombre+'" CON ID "'+str(id)+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Eliminar el Piso"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500
