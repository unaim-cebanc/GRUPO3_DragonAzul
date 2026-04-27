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
    if request.method == 'POST':
        usuario = request.form.get("usuario")
        psw = request.form.get("contrasenia")
        
        if sql_scripts.validate_user(usuario, psw):
            session["usuario"] = usuario
            return redirect(url_for("home")) # redirección placeholder
    return render_template("inicio_sesion.html")

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()