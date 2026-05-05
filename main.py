import os
from flask import Flask, render_template, request, redirect, url_for, session
import sql_scripts

app = Flask(__name__)
app.secret_key = "ABCD"
RUTA_ABSOLUTA = os.path.dirname(os.path.abspath(__file__)) 
RUTA_IMAGENES = os.path.join(RUTA_ABSOLUTA, "static", "images")
app.config["RUTA_IMAGENES"] = RUTA_IMAGENES

# Recuerda: 'py main.py' para ejecutar el servidor local y poder hacer pruebas ;)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inicio_sesion", methods = ['GET', 'POST'])
def inicio_sesion():
    session.permanent = False
    error = False
    if request.method == 'POST':
        usuario = request.form.get("usuario")
        psw = request.form.get("contrasenia")
        
        if sql_scripts.validate_user(usuario, psw):
            session["usuario"] = usuario
            return redirect(url_for("home")) # redirección placeholder
        else:
            error = True
            return render_template("inicio_sesion.html", error = error)
    return render_template("inicio_sesion.html")

@app.route("/sobre_nosotros")
def sobre_nosotros():
    return render_template("Sobre_nosotros.html")

@app.route("/recetario")
def recetario():
    recetas = sql_scripts.fetch_recepies_info()
    return render_template("recetario.html", recetas = recetas)

@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")

@app.route("/subir_receta", methods = ['GET', 'POST'])
def subir_receta():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        img = request.files["imagen"]
        img_filename = "static/images/" + img.filename
        img.save(os.path.join(RUTA_IMAGENES, img.filename))
        desc = request.form.get("descripcion")
        ingredientes = request.form.getlist("ingredientes[]")
        cantidades = request.form.getlist("cantidad[]")
        unidades = request.form.getlist("unidad[]")
        pasos = request.form.getlist("pasos[]")
        tiempo = request.form.get("tiempo_preparacion")
        tipo = request.form.get("tipo")
        id_usuario = sql_scripts.get_user_id(session.get("usuario"))
        sql_scripts.insert_recepie(nombre, img_filename, desc, ingredientes, cantidades, unidades, pasos, tiempo, tipo, id_usuario)
        return redirect(url_for("recetario"))
    return render_template("subir_receta.html", usuario = session.get("usuario")) 

@app.route("/registro", methods = ['GET', 'POST'])
def registro():
    pass_error = False
    if request.method == "POST":
        usuario = request.form.get("nombre")
        email = request.form.get("email")
        psw = request.form.get("contrasena")
        psw_check = request.form.get("contrasena_check")
        if psw != psw_check:
            pass_error = True
            return render_template("registro.html", pass_error = pass_error)
        else:
            sql_scripts.register_user(usuario, email, psw)
            return redirect(url_for("inicio_sesion"))
    return render_template("registro.html")

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()