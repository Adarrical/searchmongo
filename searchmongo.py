import pymongo
import shutil

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Catalogo"]
mycol = mydb["fotos"]

#myquery = { "IPTC:Keywords": { "$elemMatch": { "$eq": "gaia" , "$eq": "espectacle"} }  }
#myquery = { "IPTC:Keywords": { "$all":["gaia","espectacle"] } }
myquery = { "$and":[
                { "IPTC:Keywords": { "$all":["gaia"] }},
                {"EXIF:DateTimeOriginal": {"$lt":"2003-05-16"}}
                ]
          }


mydoc = mycol.find(myquery)

#Extracto los 


for x in mydoc:
  print(x['SourceFile'])
  shutil.copy(x['SourceFile'], r'c:\proyectosphyton\catalogo\resultados')

