from clases.Archivo import Archivo
from clases.Modelo import Modelo

import numpy as np
from flask import Flask, render_template, request, redirect, flash
from flask_session import Session


app = Flask(__name__)
sess = Session()
redes = Modelo()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresar')
def ingresar():
    return render_template('ingresar.html')

@app.route('/clasificar/unica', methods = ['GET', 'POST'])
def clasificaUnica():
    resena_in = request.form['reseña']
    Train = Archivo()
    Train.generarArchivoDeResenas(resena_in)
    texto = []
    for resena in Train.Resenas:
        texto.append(resena.textoResena[0])
    aspectos = [('AMBIENCE', 'GENERAL'), ('DRINKS', 'PRICES')]
    polaridades = ['Positiva', 'Negativa']
    return render_template('clasificar_unica.html', reseña = " ".join(texto), resultados = zip(aspectos,polaridades))

def formatos_permitidos(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]

    if ext.upper() in ["XML"]:
        return True
    else:
        return False


@app.route('/subir', methods=['GET', 'POST'])
def subir():
    if request.method == 'POST':
        if request.files:
            file = request.files['file']

            if not formatos_permitidos(file.filename):
                flash('Formato no permitido')
                return redirect(request.url)
            else:
                Train = Archivo()
                Train.lecturaReseñas(file)
                ### PRUEBA ####

                with open('prueba.npy', 'rb') as f:
                    wordEmbedding = np.load(f)
                [aspectos, vectores_Aspectos] = redes.obtenerAspect(wordEmbedding)
                polaridades = redes.obtenerPolaridad(wordEmbedding, vectores_Aspectos)
                pol = ['Positiva', 'Negativa', 'Neutra', 'Conflicto']
                aux = []
                for combinacion in aspectos:
                    h = []
                    for aspecto, subaspecto in combinacion:
                        h.append(aspecto + "_" +  subaspecto)
                    aux.append(h)
                aspectos = aux
                resultados_polaridad = [{}, {}, {}, {}]
                resultados_aspectos = {}
                for lista_aspecto, lista_polaridad in zip(aspectos, polaridades):
                    for aspecto, polaridad in zip(lista_aspecto, lista_polaridad):
                        posicion = pol.index(polaridad)
                        # Polaridad
                        if not aspecto in resultados_polaridad[posicion].keys():
                            resultados_polaridad[posicion][aspecto] = 1
                        else:
                            resultados_polaridad[posicion][aspecto] = resultados_polaridad[posicion][aspecto] + 1
                        # Aspecto
                        if not aspecto in resultados_aspectos.keys():
                            resultados_aspectos[aspecto] = [0, 0, 0, 0]
                            resultados_aspectos[aspecto][posicion] = 1
                        else:
                            resultados_aspectos[aspecto][posicion] = resultados_aspectos[aspecto][posicion] + 1 
                
                aux = []
                for dictPolaridad  in resultados_polaridad:
                    ordenado = list(sorted(dictPolaridad.items(), key=lambda item: item[1], reverse=True))
                    if len(ordenado) >= 5:
                        aux.append(ordenado[:5])
                    else:
                        aux.append(ordenado)
                resultados_polaridad = aux 
                return render_template('mostrar_resultados.html', aspectos = resultados_aspectos, polaridades = resultados_polaridad)
    else:
        return render_template('subir_archivo.html')

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if request.method == 'POST':
        flash('El id no existe, verifiquelo')
        return redirect(request.url)
    else:
        return render_template('consultar.html')




if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
