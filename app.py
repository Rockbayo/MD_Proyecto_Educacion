from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    datos = {
        "materia": "Minería de datos",
        "tema": "Educación, acceso y desempeño académico",
        "integrantes": [
            "Oscar Giovanni Robayo",
            "Oscar Felipe Delgado"
        ]
    }
    return render_template('index.html', **datos)

if __name__ == '__main__':
    app.run(debug=True)