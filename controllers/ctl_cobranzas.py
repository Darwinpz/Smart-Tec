from flask import jsonify, session
from database.mongodb import MongoDb
import controllers.ctl_history as hist
from controllers.validaciones import Validaciones as val
from models.cobranza import Cobranza
from bson.objectid import ObjectId
from datetime import datetime
import json

db = MongoDb().db()

def save_cobranzas(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                placa = val.val_vacio("co_placa", "", request).upper().strip()
                
                if  placa != "" :

                    existe = db.cobranzas.find_one({'placa': placa})

                    if existe:

                        if existe["salida"] != "":
                            cobranza = Cobranza(placa,datetime.now(),"",0)
                            cobranza.crear_cobranza()
                            _id = db.cobranzas.insert_one(
                                cobranza.obt()).inserted_id
                            hist.guardar_historial(
                                "CORRECTO", "CREAR", 'COBRANZA "'+placa+'" CON ID "'+str(_id)+'" CREADO CORRECTAMENTE')
                            return jsonify({"message": "Cobranza Creado Correctamente"}), 200
                        else:
                            return jsonify({"message": "Aún tiene deuda Pendiente"}), 404
                    else:
                        return jsonify({"message": "No existe vehiculo Registrado"}), 404
                else:
                    return jsonify({"message": "Información Incompleta"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "CREAR", 'ERROR AL CREAR LA COBRANZA "'+placa+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Crear la Cobranza"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def ver_cobranzas(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                cobranzas =db.cobranzas.find()
                
                data = {"data": list(cobranzas)}

                return json.dumps(data, default=str), 200
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "VISUALIZAR", 'ERROR AL VISUALIZAR TODOS LOS COBRANZAS - "'+str(e)+'"')
            return jsonify({"message": "Error al Visualizar todas los Cobranzas"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def edit_cobranzas(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                placa = val.val_vacio("co_placa", "", request).upper().strip()
                total = val.val_vacio("co_total","0",request).upper().strip()
                
                if  placa != "" and total.isdigit() :

                    existe = db.cobranzas.find_one({'placa': placa})

                    if existe:
                        cobranza = Cobranza(placa,existe["ingreso"],datetime.now(),total)
                        cobranza.update_cobranza()
                        hist.guardar_historial("CORRECTO", "ACTUALIZAR", 'COBRANZA "'+placa+'" CON ID "'+str(existe["_id"])+'" ACTUALIZADO CORRECTAMENTE')
                        return jsonify({"message": "Cobranza Creado Correctamente"}), 200
                    else:
                        return jsonify({"message": "No existe vehiculo Registrado"}), 404
                else:
                    return jsonify({"message": "Información Incompleta"}), 404
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ACTUALIZAR", 'ERROR AL ACTUALIZAR EL cobranzas "'+placa+'" CON ID "'+str(id)+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Actualizar el Piso"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500
