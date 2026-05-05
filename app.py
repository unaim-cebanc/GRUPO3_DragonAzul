from flask import Flask, render_template, request, session, redirect, url_for
import sql_scripts

app = Flask(__name__)
app.secret_key = 'clave_muy_secreta'

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        user = request.form.get('usuario')
        pw = request.form.get('contrasenia')

        usuario_valido = sql_scripts.validar_usuario(user, pw)

        if usuario_valido:
            session['usuario'] = user
            return redirect(url_for('inicio_sesion'))
        else:
            return "Usuario o contraseña incorrectos"

    return render_template('inicio_sesion.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    return redirect(url_for('inicio_sesion'))


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()