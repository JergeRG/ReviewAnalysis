import spacy
#import fasttext
#import fasttext.util
import numpy as np
import re

class Preprocesamiento:
    txtLimpio = []
    txtTokens = []
    txtVectorizado = np.array(0)
    
    def __init__(self):
        #self.ft = fasttext.load_model('cc.es.300.bin')
        self.nlp = spacy.load('es_core_news_lg')
        pass

    def obtenerTextoPre(self,resenas):
        for sentences in resenas:
            txtLimpio = self.limpieza(sentences)
            txtTokens = self.preprocessing_spacy(txtLimpio)
            #resenas.vecResena = self.get_np_vectors(txtTokens)
        return txtTokens

    def limpieza(self,Sentences):
        lstSentences = []
        if not type(Sentences) == 'list':
            return re.sub('[^.,a-zA-ZñÑáÁéÉíÍóÓúÚ0-9. \n\.]', '', Sentences)
        else:
            for sentence in Sentences:
                lstSentences.append(re.sub('[^.,a-zA-ZñÑáÁéÉíÍóÓúÚ0-9. \n\.]', '', sentence))
            return lstSentences
    
    def preprocessing_spacy(self,Sentences):
        # Cargar modelo pre entrenado
        s_lemma = []
        # Procesar Oraciones
        for sentences in Sentences:
            doc = nlp(sentences)
            lemma = list()
            for token in doc:
                if token.is_space or token.is_punct:
                    pass
                else:
                    lemma.append(token.lemma_)
            s_lemma.append(lemma)
        return s_lemma
                
    '''
    def get_np_vectors(self,Sentences):
       
        x_vec = []
        vec = np.array(0)
        for sentence in Sentences:
            vec = vec + ft.get_sentence_vector(" ".join(sentence))
        x_vec.append(vec)

        X_set = np.asarray(x_vec)
        X_set = X_set.reshape(len(X_set),ft.get_dimension(),1)

        return X_set
'''