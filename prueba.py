from flask import Flask, render_template, request, redirect, url_for, session
import sql_scripts

app = Flask(__name__)
app.secret_key = "ABCD"

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

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()