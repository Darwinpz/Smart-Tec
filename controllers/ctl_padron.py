from flask import jsonify
from database.mongodb import MongoDb
from controllers.validaciones import Validaciones as val
import json
db = MongoDb().db()

def buscar(request):

    if request.method == 'POST':

        cedula = val.val_vacio("s_buscar","",request).strip()

        ciudadano = db.padron_2023.find_one({"cedula": cedula})

        if ciudadano:
            return json.dumps(ciudadano, default=str), 200
        else:
            return jsonify({"message": "Ciudadano no encontrado"}), 400
    else:
        return jsonify({"message": "Petición Incorrecta"}), 500
