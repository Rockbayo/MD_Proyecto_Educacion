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

if __name__ == '__main__':
    app.run(debug=True)