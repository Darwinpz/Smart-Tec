from flask import jsonify, session
from database.mongodb import MongoDb
import controllers.ctl_history as hist
from controllers.validaciones import Validaciones as val
from models.sensor import Sensor
from bson.objectid import ObjectId
import json

db = MongoDb().db()

def save_sensores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                piso = val.val_vacio("s_piso", "", request).upper().strip()
                seccion = val.val_vacio("s_seccion", "", request).upper().strip()
                plaza = val.val_vacio("s_plaza", "", request).upper().strip()
                nombre = val.val_vacio("s_nombre", "", request).upper().strip()
                
                if  nombre != "":

                    existe = db.sensores.find_one(
                        {"$or": [{'nombre': nombre}]})

                    if existe:
                        return jsonify({"message": "Piso Existente"}), 404
                    else:
                        sensor = Sensor(ObjectId(piso), seccion, plaza, nombre, "DESCONECTADO")
                        sensor.crear_sensor()
                        _id = db.sensores.insert_one(sensor.obtener_sensor()).inserted_id
                        hist.guardar_historial(
                            "CORRECTO", "CREAR", 'SENSOR "'+nombre+'" CON ID "'+str(_id)+'" CREADO CORRECTAMENTE')
                        return jsonify({"message": "Sensor Creado Correctamente"}), 200
                else:
                    return jsonify({"message": "Información Incompleta"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "CREAR", 'ERROR AL CREAR EL SENSOR "'+nombre+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Crear el Sensor"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def ver_sensores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                sensores = db.sensores.aggregate([
                        {"$lookup": {"from": "pisos", "localField": "piso",
                                     "foreignField": "_id", "as": "piso"}},
                        {"$unwind": "$piso"}
                    ])
                
                data = {"data": list(sensores)}
                
                return json.dumps(data, default=str), 200
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "VISUALIZAR", 'ERROR AL VISUALIZAR TODOS LOS SENSORES - "'+str(e)+'"')
            return jsonify({"message": "Error al Visualizar todos los Sensores"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def edit_sensores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                piso = val.val_vacio("s_piso", "", request).upper().strip()
                seccion = val.val_vacio("s_seccion", "", request).upper().strip()
                plaza = val.val_vacio("s_plaza", "", request).upper().strip()
                nombre = val.val_vacio("s_nombre", "", request).upper().strip()

                id = val.val_vacio("s_codigo", "", request).strip()

                existe = db.sensores.find_one({"_id": ObjectId(id)})

                if existe:

                    existe_nombre = db.sensores.find_one(
                        {"nombre": nombre})

                    if existe_nombre:
                        if existe_nombre["_id"] != existe["_id"]:
                            return jsonify({"message": "No se puede actualizar, sensor Existente"}), 404

                    sensor = Sensor(ObjectId(piso), seccion, plaza, nombre, "DESCONECTADO")
                    sensor.update_piso()
                    db.sensores.update_one({"_id": ObjectId(id)}, {
                        "$set": sensor.obtener_piso()})
                    hist.guardar_historial(
                        "CORRECTO", "ACTUALIZAR", 'SENSOR "'+nombre + '" CON ID "'+str(id)+'" ACTUALIZADO CORRECTAMENTE')
                    return jsonify({"message": "Sensor Actualizado Correctamente"}), 200
                else:
                    return jsonify({"message": "Sensor No existe"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ACTUALIZAR", 'ERROR AL ACTUALIZAR EL SENSOR "'+nombre+'" CON ID "'+str(id)+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Actualizar el Sensor"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def del_sensores(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                id = val.val_vacio("id", "", request).strip()
                nombre = val.val_vacio("s_nombre", "", request).upper().strip()
                existe = db.sensores.find_one({"_id": ObjectId(id)})

                if existe:

                    db.sensores.delete_one({"_id": ObjectId(id)})
                    hist.guardar_historial(
                            "CORRECTO", "ELIMINAR", 'SENSOR "'+nombre+'" CON ID "'+str(id)+'" ELIMINADO CORRECTAMENTE')
                    return jsonify({"message": "Sensor Eliminado Correctamente"}), 200
                        
                else:
                    return jsonify({"message": "Sensor NO Existente"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ELIMINAR", 'ERROR AL ELIMINAR EL SENSOR "'+nombre+'" CON ID "'+str(id)+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Eliminar el Sensor"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500
