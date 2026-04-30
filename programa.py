from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/recetas')
def listar_recetas():
    # Obtenemos el tipo de la URL, por defecto 'todas'
    tipo_filtro = request.args.get('tipo', 'todas').lower()

    if tipo_filtro == 'vegana':
        # Aprovechamos la vista especializada
        recetas = VistaRecetaVegana.query.all()
    elif tipo_filtro == 'vegetariana':
        recetas = Receta.query.filter_by(tipo='vegetariana').all()
    elif tipo_filtro == 'normal':
        recetas = Receta.query.filter_by(tipo='normal').all()
    else:
        recetas = Receta.query.all()

    return render_template('todas.html', recetas=recetas, filtro=tipo_filtro)