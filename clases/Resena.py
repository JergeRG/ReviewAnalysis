
from pymongo import MongoClient
import numpy as np
 
class Resena:
    id_Resena = ''
    textoResena = []
    aspectos = []
    polaridad = []
    vecResena = [] #np.array(0) 
    fecha = ''

    def __init__(self,id,text,aspectos=[],polaridad=[],vec=[],fecha='0'):
        self.id_Resena = id
        self.textoResena = text
        self.aspectos = aspectos
        self.polaridad = polaridad
        self.vecResena = vec
        self.fecha = fecha
    
   

    def cargaResenaPrevia(self,id):
        #self.textoResena, self.aspectos, self.polaridad = self.db.consultarReseña(id)
        pass


    