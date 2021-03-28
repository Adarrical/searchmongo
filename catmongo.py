import exiftool
import os 
import pymongo

#LLena la base de datos mongodb foto d:\mongodb"

CARPETA_INICIO = 'd:/imagenes'

#Conectcamos a la base de datos .
myclient = pymongo.MongoClient("mongodb://localhost")
mydb = myclient["Catalogo"]
mycol = mydb["fotos"]

list_files=[]
print("Selecting files .................... ")
for base, dirs, files in os.walk(CARPETA_INICIO): 
    if 'Por Procesar' in base or 'Showroom' in base or 'Stock' in base or 'Portada disc' in base or 'texturas' in base or 'Documentació' in base or 'CaptureOne' in base:
        pass
    else:
        for f in files: 
            nombre_archivo, extension = os.path.splitext(f)
            if extension.upper() == '.JPG' or extension.upper() == '.TIF':
                list_files.append(base+'\\'+f)

print("Extracting and save files metadata..........be patient my friend........ ")
with exiftool.ExifTool() as et:
    metadata = et.get_metadata_batch(list_files)
    for m in metadata:
        try: 
            m['IPTC:Keywords'] = [element.lower() for element in m['IPTC:Keywords']]
        except: 
            print("Sin palabras clave")
        x = mycol.insert_one(m)


    



