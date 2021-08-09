from pymongo import MongoClient

from Archivo import Archivo
from Resenas import Resena


class Almacenamiento:
    client = MongoClient('localhost')
    db = client['ABSArESEÑAS']
    

    def almacenar(self,col,id,txt,aspect,pol,vec):
        collecion = self.db[col]
        collecion.insert_one({
            '_id':id,
            'Sentences':txt,
            'Aspects':aspect,
            'Polarities': pol,
            'Vector':vec
        })

    def consultarReseña(self,col):
        Arc = Archivo()
        Arc.id_file = col
        collecion = self.db[col]
        for file in collecion.find({}):
            Arc.Resenas.append(Resena(file['id'],file['Sentences'],file['Aspects'],file['Polarities'],file['Vector']))
        
        return Arc
