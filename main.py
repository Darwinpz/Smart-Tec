from flask import Flask, request, render_template
from dotenv import load_dotenv
import controllers.ctl_servidor as serv
import controllers.index as ini
import controllers.ctl_history as hist
import controllers.ctl_piso as piso
import controllers.ctl_usuario as user
import controllers.ctl_padron as ctl_padron
import controllers.ctl_sensor as sensor
import controllers.ctl_clientes as cli
import controllers.ctl_cobranzas as co
import os 

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.getenv("KEY")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# -----RUTAS---------------------------------------------

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# ---INDEX---

@app.route('/', methods=['GET', 'POST'])
def index():
    return ini.index(request)

@app.route('/principal', methods=['GET'])
def principal():
    return ini.principal()

# ---PADRON---


@app.route('/padron/buscar', methods=['POST'])
def padron_buscar():
    return ctl_padron.buscar(request)


# ----- PISOS -----

@app.route('/principal/save_pisos', methods=['POST'])
def save_pisos():
    return piso.save_pisos(request)


@app.route('/principal/ver_pisos', methods=['POST'])
def ver_pisos():
    return piso.ver_pisos(request)


@app.route('/principal/edit_piso', methods=['POST'])
def edit_pisos():
    return piso.edit_pisos(request)


@app.route('/principal/del_pisos', methods=['POST'])
def del_pisos():
    return piso.del_pisos(request)

# ----- SENSORES -----

@app.route('/principal/save_sensores', methods=['POST'])
def save_sensores():
    return sensor.save_sensores(request)


@app.route('/principal/ver_sensores', methods=['POST'])
def ver_sensores():
    return sensor.ver_sensores(request)


@app.route('/principal/edit_sensor', methods=['POST'])
def edit_sensores():
    return sensor.edit_sensores(request)


@app.route('/principal/del_sensores', methods=['POST'])
def del_sensores():
    return sensor.del_sensores(request)


# ---- SERVIDORES ---

@app.route('/principal/save_servidores', methods=['POST'])
def save_servidores():
    return serv.save_servidores(request)


@app.route('/principal/ver_servidores', methods=['POST'])
def ver_servidores():
    return serv.ver_servidores(request)


@app.route('/principal/edit_servidor', methods=['POST'])
def edit_servidor():
    return serv.edit_servidores(request)


@app.route('/principal/del_servidores', methods=['POST'])
def del_servidores():
    return serv.del_servidores(request)

# ---- CLIENTES ---

@app.route('/principal/save_clientes', methods=['POST'])
def save_clientes():
    return cli.save_clientes(request)


@app.route('/principal/ver_clientes', methods=['POST'])
def ver_clientes():
    return cli.ver_clientes(request)


@app.route('/principal/edit_cliente', methods=['POST'])
def edit_cliente():
    return cli.edit_clientes(request)


@app.route('/principal/del_clientes', methods=['POST'])
def del_clientes():
    return cli.del_clientes(request)


# ---- COBRANZA ---

@app.route('/principal/save_cobranzas', methods=['POST'])
def save_cobranzas():
    return co.save_cobranzas(request)


@app.route('/principal/ver_cobranzas', methods=['POST'])
def ver_cobranzas():
    return co.ver_cobranzas(request)

@app.route('/principal/edit_cobranza', methods=['POST'])
def edit_cobranza():
    return co.edit_cobranzas(request)

# ----- USUARIOS ---------

@app.route('/principal/save_usuarios', methods=['POST'])
def save_usuarios():
    return user.save_usuarios(request)


@app.route('/principal/ver_usuarios', methods=['POST'])
def ver_usuarios():
    return user.ver_usuarios(request)


@app.route('/principal/edit_usuario', methods=['POST'])
def edit_usuario():
    return user.edit_usuarios(request)


@app.route('/principal/del_usuarios', methods=['POST'])
def del_usuarios():
    return user.del_usuarios(request)


#--- HISTORIES --
@app.route('/principal/ver_histories', methods=['POST'])
def hist_ver_histories():
    return hist.ver_history(request)


@app.route('/salir')
def salir():
    return ini.cerrar_sesion()

# -----ERRORES---------------

@app.errorhandler(500)
def handle_500(e):
    return render_template('/views/errors/500.html')


@app.errorhandler(401)
def handle_401(e):
    return render_template('/views/errors/401.html')

@app.errorhandler(404)
def handle_404(e):
    return render_template('/views/errors/404.html')


@app.errorhandler(403)
def handle_403(e):
    return render_template('/views/errors/403.html')

# -----------------------------


if __name__ == '__main__':
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))
