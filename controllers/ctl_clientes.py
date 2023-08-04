from flask import jsonify, session
from database.mongodb import MongoDb
import controllers.ctl_history as hist
from controllers.validaciones import Validaciones as val
from models.cliente import Cliente
from bson.objectid import ObjectId
import controllers.encrypt as encrypt
import json

db = MongoDb().db()

def save_clientes(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                if session["rol"] == "Administrador" or session["rol"] == "Super-Admin":

                    cedula = val.val_vacio("cli_cedula","",request).upper().strip()
                    nombre = val.val_vacio("cli_ciudadano","",request).upper().strip()
                    correo = val.val_vacio("cli_correo","",request).lower().strip()
                    placa = val.val_vacio("cli_placa","",request).upper().strip()
                    clave = val.val_vacio("cli_clave","",request)
                    rep_clave = val.val_vacio("cli_rep_clave","",request)

                    if cedula != "" and nombre != "" and correo != "" and  placa != "" and clave != "" and rep_clave != "":

                        if clave == rep_clave:

                            existe = db.clientes.find_one({'cedula': cedula})

                            if existe:
                                return jsonify({"message": "Cliente Existente"}), 404
                            else:
                                clave = encrypt.encrypt(clave)
                                cliente = Cliente(cedula, clave, nombre, correo, placa)
                                cliente.crear_cliente()
                                _id = db.clientes.insert_one(
                                    cliente.obtener_cliente()).inserted_id
                                hist.guardar_historial(
                                    "CORRECTO", "CREAR", 'cliente "'+nombre+'" CON ID "'+str(_id)+'" CREADO CORRECTAMENTE')
                                return jsonify({"message": "cliente Creado Correctamente"}), 200
                        else:
                            return jsonify({"message": "Las Claves no Coinciden"}), 404
                    else:
                        return jsonify({"message": "Información Incompleta"}), 404
                else:
                    return jsonify({"message": "Debes ser Administrador"}), 401
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "CREAR", 'ERROR AL CREAR EL cliente "'+nombre+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Crear el cliente"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def ver_clientes(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                if session["rol"] == "Administrador" or session["rol"] == "Super-Admin":

                    clientes = db.clientes.find({})

                    datos = list(clientes)

                    for us in datos:
                        us["clave"] = encrypt.decrypt(us["clave"])

                    data = {"data": datos}

                    return json.dumps(data, default=str), 200
                else:
                    return jsonify({"message": "Debes ser Administrador"}), 401
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "VISUALIZAR", 'ERROR AL VISUALIZAR TODOS LOS CLIENTES - "'+str(e)+'"')
            return jsonify({"message": "Error al Visualizar todos los Clientes"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def edit_clientes(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                if session["rol"] == "Administrador" or session["rol"] == "Super-Admin":

                    cedula = val.val_vacio("cli_cedula","",request).upper().strip()
                    nombre = val.val_vacio("cli_ciudadano","",request).upper().strip()
                    correo = val.val_vacio("cli_correo","",request).lower().strip()
                    placa = val.val_vacio("cli_placa","",request).upper().strip()
                    clave = val.val_vacio("cli_clave","",request)
                    rep_clave = val.val_vacio("cli_rep_clave","",request)

                    if cedula != "" and nombre != "" and correo != "" and  placa != "" and clave != "" and rep_clave != "":

                        if clave == rep_clave:

                            existe = db.clientes.find_one({'cedula': cedula})

                            if existe:

                                clave = encrypt.encrypt(clave)
                                cliente = Cliente(cedula, clave, nombre, correo, placa)
                                cliente.update_cliente()
                                db.clientes.update_one({"_id": ObjectId(existe["_id"])}, {
                                    "$set": cliente.obtener_cliente()})
                                hist.guardar_historial(
                                    "CORRECTO", "ACTUALIZAR", 'CLIENTE "'+cedula+'" ACTUALIZADO CORRECTAMENTE')
                                return jsonify({"message": "Cliente Actualizado Correctamente"}), 200

                            else:
                                return jsonify({"message": "Cliente No Existente"}), 404
                        else:
                            return jsonify({"message": "Las Claves no Coinciden"}), 404
                    else:
                        return jsonify({"message": "Información Incompleta"}), 404
                else:
                    return jsonify({"message": "Debes ser Administrador"}), 401
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ACTUALIZAR", 'ERROR AL ACTUALIZAR EL cliente "'+cedula+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Actualizar el cliente"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500


def del_clientes(request):

    if request.method == 'POST':

        try:

            if val.validar_session(session):

                if session["rol"] == "Administrador" or session["rol"] == "Super-Admin":

                    cedula = val.val_vacio("cedula","",request).upper().strip()
                    existe = db.clientes.find_one({"cedula": cedula})

                    if existe:
                        db.clientes.delete_one({"cedula": cedula})
                        hist.guardar_historial(
                            "CORRECTO", "ELIMINAR", 'CLIENTE "'+cedula+'" ELIMINADO CORRECTAMENTE')
                        return jsonify({"message": "Cliente Eliminado Correctamente"}), 200
                    else:
                        return jsonify({"message": "Cliente NO Existente"}), 404
                else:
                    return jsonify({"message": "Debes ser Administrador"}), 401
            else:
                return jsonify({"message": "Debes iniciar sesión"}), 403
        except Exception as e:
            hist.guardar_historial(
                "ERROR", "ELIMINAR", 'ERROR AL ELIMINAR EL CLIENTE "'+cedula+'" - "'+str(e)+'"')
            return jsonify({"message": "Error al Eliminar el Cliente"}), 404
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500
