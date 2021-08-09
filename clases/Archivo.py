import xml.etree.ElementTree as ET 
import csv
from os import path 
from clases.Resena import Resena


class Archivo:
    id_file = ''
    cantResenas = 0
    Resenas = []

    def generarArchivoDeResenas(self,resena):
        self.id_file = '45'
        self.cantResenas = 1
        self.Resenas = []
        self.Resenas.append(Resena('44',resena.split('. ')))
    
    def lecturaReseñas(self,file):
        data = file.read()
        tree = ET.fromstring(data)

        totalReviews = 0
        for review in tree.findall('Review'):
            totalReviews = totalReviews + 1 
            rid = review.get('rid')
            lstSentence = []
            for sentence in review.find('sentences').findall('sentence'):         
                lstSentence.append(sentence.find('text').text)
    
            self.Resenas.append(Resena(rid,lstSentence))

        self.cantResenas=totalReviews
        self.id_file= '54'
        
    def extractTree(self,folder):
        with open(folder, 'r') as file:
            data = file.read()
        return ET.fromstring(data)
    
    