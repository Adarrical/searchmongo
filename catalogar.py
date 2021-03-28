import exiftool
import os 
import sqlite3
from sqlite3 import Error 
from decimal import Decimal
import datetime 

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e: 
        print(e)

    return conn

def quitar_foto_del_catalogo(foto, conn): 
    cur=conn.cursor()
    sql = 'delete from fotos where sourcefile=?'
    cur.execute(sql, (foto,))

    sql = 'delete from fotos_kw where sourcefile=?'
    cur.execute(sql, (foto,))
    conn.commit()


def anyadir_foto_al_catalogo(metadata, conn):  
    sql = 'insert into fotos values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    sourcefile = metadata['SourceFile']
    filesize = int(metadata['File:FileSize'])
    imagewidth = int(metadata['File:ImageWidth'])
    imageheight = int(metadata['File:ImageHeight'])
    try:
        make = metadata['EXIF:Make']
    except KeyError: 
        make = ''
    
    try:
        model = metadata['EXIF:Model']
    except KeyError: 
        model = ''
    
    try:
        exposuretime = Decimal(metadata['EXIF:ExposureTime'])
    except KeyError: 
        exposuretime = 0

    try:
        fnumber=float(metadata['EXIF:FNumber'])
    except KeyError: 
        fnumber = 0 

    if fnumber == 0: 
        try: 
            fnumber = float(metadata['EXIF:ApertureValue'])
        except KeyError: 
            fnumber = 0 
    
    try:
        iso = int(metadata['EXIF:ISO'])
    except KeyError: 
        iso = 0

    try:
        creationdate = datetime.datetime.strptime(metadata['EXIF:CreateDate'], '%Y:%m:%d %H:%M:%S')
    except KeyError: 
        creationdate = ''
    
    try:
        compensation = float(metadata['EXIF:ExposureCompensation'])
    except KeyError: 
        compensation = 0
    
    try:
        lensmake = metadata['EXIF:LensMake']
    except KeyError:
        lensmake = ''
       
    try:
        lensmodel = metadata['EXIF:LensModel']
    except KeyError: 
        lensmodel = ''
    
    try:
        titulo = metadata['XMP:Description'] 
    except KeyError: 
        titulo = ''
    
    cur=conn.cursor()

    cur.execute(sql,(sourcefile, 
                     filesize, 
                     titulo,
                     imagewidth,
                     imageheight,
                     make,
                     model,
                     float(exposuretime),
                     fnumber,
                     iso,
                     creationdate,
                     compensation,
                     lensmake,
                     lensmodel
                     ))
    
    conn.commit()

def anyadir_kw_al_catalogo(m,conn):
    sourcefile = m['SourceFile']
    sql = 'insert into fotos_kw values (?,?)'
    cur=conn.cursor()
   
    try: 
        lista_kw = m['IPTC:Keywords']
        for l in lista_kw: 
            cur.execute(sql,(sourcefile, l))
        conn.commit() 
    except KeyError: 
        pass 
    


database = 'd:\\sqlite\\catalogo\\catalogo.db'
carpeta_inicio = 'd:/imagenes'

conn = create_connection(database)


list_files=[]
print("Selecting files .................... ")
for base, dirs, files in os.walk(carpeta_inicio): 
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
        quitar_foto_del_catalogo(m['SourceFile'], conn)
        anyadir_foto_al_catalogo(m, conn)
        anyadir_kw_al_catalogo(m, conn) 
        
    



