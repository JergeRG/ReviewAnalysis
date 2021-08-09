from Archivo import Archivo
from Preprocesamiento import Preprocesamiento
from Modelo import Modelo
from Almacenamiento import Almacenamiento


Train = Archivo()
TrainP = Preprocesamiento()
Modelos = Modelo()
Save = Almacenamiento()

'''
## Si es solo una reseña
resena_in = 'Reseña de entrada. Para cuando es solo una reseña.'
Train.generarArchivoDeResenas(resena_in)
## Si es archivo
#Train.lecturaReseñas('sp_restaurants_trial_sb2.xml')

# Preprocesamiento

for review in Train.Resenas:
    review.vecResena = TrainP.obtenerTextoPre(review.textoResena)

# Modelo
for review in Train.Resenas:
    review.aspectos = Modelos.obtenerAspect(review.vecResena)

for review in Train.Resenas:
    review.polaridad = Modelos.obtenerPolaridad(review.vecResena,review.aspectos)

# Almacenamiento
for review in Train.Resenas:
    Save.almacenar(Train.id_file,review.id_Resena,review.textoResena,review.aspectos,review.polaridad,review.vecResena)
'''
# Si solo se consulta
Train = Save.consultarReseña('TrialSet')


for review in Train.Resenas:
    print(review.Sentences)


