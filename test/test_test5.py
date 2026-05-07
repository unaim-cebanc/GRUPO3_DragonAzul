import sql_scripts
import pytest
from flask import Flask, render_template, request, redirect, url_for, session

class PaginaWeb:
    def home():
        return render_template("index.html")

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
    
    def sobre_nosotros():
        return render_template("Sobre_nosotros.html")
    
    def recetario():
    # ERROR: se llama a fetch_recepies_info() con un argumento de más.
    # Esta función no acepta parámetros, por lo que lanzará un TypeError en tiempo de ejecución.
        recetas = sql_scripts.fetch_recepies_info(True)
        return render_template("recetario.html", recetas = recetas)
