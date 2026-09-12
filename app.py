from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/etapa1/problema')
def problema():
    return render_template('etapa1/problema.html')

@app.route('/etapa1/preguntas')
def preguntas():
    return render_template('etapa1/preguntas.html')

@app.route('/etapa1/necesidades')
def necesidades():
    return render_template('etapa1/necesidades.html')

@app.route('/etapa1/fuentes')
def fuentes():
    return render_template('etapa1/fuentes.html')

@app.route('/etapa1/dataset')
def dataset():
    return render_template('etapa1/dataset.html')

@app.route('/etapa1/diccionario')
def diccionario():
    return render_template('etapa1/diccionario.html')

@app.route('/etapa1/calidad')
def calidad():
    return render_template('etapa1/calidad.html')

@app.route('/etapa1/limitaciones')
def limitaciones():
    return render_template('etapa1/limitaciones.html')

# ==========================================
# RUTAS ETAPA 2: DIAGNÓSTICO Y CALIDAD
# ==========================================
@app.route('/etapa2/proposito')
def proposito():
    return render_template('etapa2/proposito.html')

@app.route('/etapa2/perfilamiento')
def perfilamiento():
    return render_template('etapa2/perfilamiento.html')

@app.route('/etapa2/dimensiones')
def dimensiones():
    return render_template('etapa2/dimensiones.html')

@app.route('/etapa2/integracion')
def integracion():
    return render_template('etapa2/integracion.html')

@app.route('/etapa2/informe')
def informe():
    return render_template('etapa2/informe.html')

if __name__ == '__main__':
    app.run(debug=True)