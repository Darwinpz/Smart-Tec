from flask import Flask, request, render_template
from dotenv import load_dotenv
import controllers.ctl_servidor as serv
import controllers.index as ini
import controllers.ctl_history as hist
import controllers.ctl_usuario as user
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
