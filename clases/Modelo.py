import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_addons as tfa

class Modelo:
    # Carga de modelo de sentimientos
    model_aspects = keras.models.load_model('clases/Modelos/Aspects_NN_624/Aspects_NN_644.h5')
    

    # Carga de modelo
    model_polarity = keras.models.load_model('clases/Modelos/Polarity_CNN_300/my_model.h5')

    aspectos = [('AMBIENCE', 'GENERAL'),
    ('DRINKS', 'PRICES'),
    ('DRINKS', 'QUALITY'),
    ('DRINKS', 'STYLE_OPTIONS'),
    ('FOOD', 'PRICES'),
    ('FOOD', 'QUALITY'),
    ('FOOD', 'STYLE_OPTIONS'),
    ('LOCATION', 'GENERAL'),
    ('RESTAURANT', 'GENERAL'),
    ('RESTAURANT', 'MISCELLANEOUS'),
    ('RESTAURANT', 'PRICES'),
    ('SERVICE', 'GENERAL')]
    
    polaridad = ['Positiva', 'Negativa', 'Neutra', 'Conflicto']

    def obtenerAspect(self,X):

        # Prediccion de modelo
        y = self.model_aspects.predict(X,verbose=0)

        # Aplicando umbral de decicion
        y_1 = []
        
        # Solo 1 salida
        if y.ndim == 1:
            y_1 = [int(x) for x in y > 0.85]
        
        # Multiples salidas
        else:
            for i in y:
                y_1.append([int(x) for x in i >0.85])
        
        y_1 = np.asarray(y_1,dtype='float32')
        
        # Obteniendo string
        
        y_aspectos = []
        
        if y_1.ndim == 1:
            for j in np.where(y_1 == 1.)[0].tolist():
                y_aspectos.append(self.aspectos[j])

        else:
            for i in y_1:
                h = []
                for j in np.where(i == 1.)[0].tolist():
                    h.append(self.aspectos[j])
                y_aspectos.append(h)
        
        return y_aspectos, y_1

    def obtenerPolaridad(self,wordEmbedding, aspectos):

        # Formato de el vector de entrada 
        X = []
        for aspecto, embeddings in zip(aspectos, wordEmbedding):
            pos = np.where(aspecto == 1)[0]
            if len(pos):
                for index in pos:
                    vector = [0] * 12
                    vector[index] = 1
                    X = np.append(X, np.asanyarray(embeddings.reshape(300).tolist() + vector))
            else:
                X = np.append(X, np.asanyarray(embeddings.reshape(300).tolist() + [0]*12))
        
        X = X.reshape(len(X)//312,312,1)
        y = self.model_polarity.predict(X,verbose=0)
        
        y_1 = []
        # Solo 1 salida
        if y.shape[0] == 1:
            y_1 = [0] *4
            y_1[np.where(y == max(y))[0][0]] = 1
        
        # Multiples salidas
        else:
            for i in y:
                aux = [0] * 4
                aux[np.where(i == max(i))[0][0]] = 1
                y_1.append(aux)
        
        y_1 = np.asarray(y_1,dtype='float32')

        y_polaridad = []
        
        if y_1.shape[0] == 1:
            for j in np.where(y_1 == 1.)[0].tolist():
                y_polaridad.append(self.polaridad[j])

        else:
            for i in y_1:
                h = []
                for j in np.where(i == 1.)[0].tolist():
                    h.append(self.polaridad[j])
                y_polaridad.append(h)
        
        return y_polaridad
        
