import pymongo
import shutil
import sys
import json
from PyQt5 import uic, QtWidgets, QtCore #Importamos módulo uic y Qtwidgets
from PyQt5.QtGui import QPixmap


qtCreatorFile = "searchmongo.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class VentanaPrincipal(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self): #Constructor de la clase
        QtWidgets.QMainWindow.__init__(self) #Constructor
        Ui_MainWindow.__init__(self) #Constructor
        self.setupUi(self) # Método Constructor de la ventana

        self.le_values.installEventFilter(self)
        
        self.le_labels.installEventFilter(self)

        self.btn_and.clicked.connect(self.boton_and)    

        self.btn_or.clicked.connect(self.boton_or)    

        self.btn_gt.clicked.connect(self.boton_gt)    

        self.btn_gte.clicked.connect(self.boton_gte)    

        self.btn_lt.clicked.connect(self.boton_lt)    

        self.btn_lte.clicked.connect(self.boton_lte)    

        self.btn_ne.clicked.connect(self.boton_ne)    

        self.btn_labels.clicked.connect(self.boton_labels)    

        self.btn_create_date.clicked.connect(self.boton_create_date)    

        self.btn_sourcefile.clicked.connect(self.boton_sourcefile)    

        self.btn_filename.clicked.connect(self.boton_filename)    

        self.btn_directory.clicked.connect(self.boton_directory)

        self.btn_make.clicked.connect(self.boton_make)

        self.btn_model.clicked.connect(self.boton_model)

        self.btn_copyright.clicked.connect(self.boton_copyright)

        self.btn_exposuretime.clicked.connect(self.boton_exposuretime)

        self.btn_iso.clicked.connect(self.boton_iso)

        self.btn_aperture_value.clicked.connect(self.boton_aperture_value)

        self.btn_focal_lenght.clicked.connect(self.boton_focal_lenght)

        self.btn_focal_lenght_35.clicked.connect(self.boton_focal_lenght_35)

        self.btn_lens_model.clicked.connect(self.boton_lens_model)


        self.btn_clear_query.clicked.connect(self.boton_clear_query)

        self.btn_eq.clicked.connect(self.boton_eq) 

        self.btn_end_query.clicked.connect(self.boton_end_query)

        self.btn_run_query.clicked.connect(self.boton_run_query)
        
        self.texto_ant = ""

        self.cb_or.setVisible(False)
        
            
    def boton_and(self):
        #if self.lbl_query.text() != '{"$and":[' :
        #    self.lbl_query.setText(self.lbl_query.text() + ']},')
        if self.le_values.text():
            self.lbl_query.setText(self.lbl_query.text() + ']},')

        self.cb_or.setChecked(False)
        self.lbl_query.setText(self.lbl_query.text() +  "\n"   + '{"$or":[')
        
    def boton_or(self): 
        self.lbl_query.setText(self.lbl_query.text() + ',' )
        self.cb_or.setChecked(True)
        
    
    def boton_eq(self):
        self.lbl_query.setText(self.lbl_query.text() + '"$eq":')

    def boton_gt(self):
        self.lbl_query.setText(self.lbl_query.text() + '"$gt":')

    def boton_gte(self):
        self.lbl_query.setText(self.lbl_query.text() + '"$gte":')

    def boton_lt(self):
        self.lbl_query.setText(self.lbl_query.text() + '"$lt":')

    def boton_lte(self):
        self.lbl_query.setText(self.lbl_query.text() + '"$lte":')

    def boton_ne(self):
        self.lbl_query.setText(self.lbl_query.text() + '"$ne":')

    def boton_create_date(self): 
        self.lbl_hlp.setText('Enter create date format as "aaaa:mm:dd"')
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:CreateDate":{')

    def boton_sourcefile(self): 
        self.lbl_hlp.setText('Enter sourcefile between quotes " " path + namefile ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"Sourcefile":{')
 
    def boton_filename(self): 
        self.lbl_hlp.setText('Enter filename between quotes " " namefile + ext. ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"File:FileName":{')

    def boton_directory(self): 
        self.lbl_hlp.setText('Enter filename between quotes " " unit:+directory ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"File:Directory":{')
    
    def boton_make(self):
        self.lbl_hlp.setText('Enter cammera name between quotes " "' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:Make":{')

    def boton_model(self):
        self.lbl_hlp.setText('Enter model of cammera between quotes " "' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:Model":{')
    
    def boton_copyright(self):
        self.lbl_hlp.setText('Enter copyright between quotes " "' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:Copyright":{')

    def boton_exposuretime(self): 
        self.lbl_hlp.setText('Enter exposure time as decimmal number without quotes " " ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"Exif:ExposureTime":{')

    def boton_iso(self): 
        self.lbl_hlp.setText('Enter ISO as number without quotes " " ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:ISO":{')

    def boton_aperture_value(self):
        self.lbl_hlp.setText('Enter aperture value as decimal number without quotes " " ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:ApertureValue":{')

    def boton_focal_lenght(self): 
        self.lbl_hlp.setText('Enter focal lenght as decimmal number without quotes " " ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:FocalLength":{')

    def boton_focal_lenght_35(self):
        self.lbl_hlp.setText('Enter focal lenght 35mm  as decimmal number without quotes " " ' )
        self.lbl_query.setText(self.lbl_query.text() + '{"EXIF:FocalLengthIn35mmFormat":{')

    def boton_lens_model(self):
        self.lbl_hlp.setText('Enter lens model between quotes " " ' )
        self.lbl_query.setText(self.lbl_query.text() + '{EXIF:LensModel":{')
   

    def boton_clear_query(self): 
        self.lbl_query.setText('{"$and":[')
        self.cb_or.setChecked(False)
        self.le_values.setText("")
        self.le_labels.setText("")

    def boton_run_query(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Catalogo"]
        mycol = mydb["fotos"]
        
        myquery = json.loads(self.lbl_query.text())
        
        mydoc = mycol.find(myquery)

        
        for x in mydoc:
            shutil.copy(x['SourceFile'], r'c:\proyectosphyton\catalogo\resultados')

    def boton_labels(self):
        self.lbl_hlp.setText('Enter labels in lowercase separated by comma without quotes' )
       
    def set_etiquetas(self): 
        if self.le_labels.text == '': 
            return False
        texto = ""
    
        lista_etiquetas = self.le_labels.text().split(",")
        self.lbl_query.setText(self.lbl_query.text() + "\n" + '{"$or":[')
        
        numero_etiqueta = 0
        if self.rb_all.isChecked(): 
            self.lbl_query.setText(self.lbl_query.text() + '{ "IPTC:Keywords": { "$all":[')
            for etiqueta in lista_etiquetas:
                numero_etiqueta += 1 
                if numero_etiqueta < len(lista_etiquetas):
                    texto += '"' + etiqueta + '"' + ','
                else: 
                    texto += '"' + etiqueta + '"]}}]},'

        if self.rb_or.isChecked(): 
            for etiqueta in lista_etiquetas: 
                numero_etiqueta += 1 
                if numero_etiqueta < len(lista_etiquetas): 
                    texto += '{ "IPTC:Keywords": ' + '"' + etiqueta + '"},'
                else: 
                    texto += '{ "IPTC:Keywords": ' + '"' + etiqueta + '"}]},'

        self.lbl_query.setText(self.lbl_query.text()  + texto )
        
        return True

    def boton_end_query(self): 
        self.lbl_query.setText(self.lbl_query.text() + ']}]}')
        self.cb_or.setChecked(False)
        
    def eventFilter(self, obj, evt):
        if obj.objectName() == "le_values" and evt.type() == QtCore.QEvent.FocusIn:
            self.texto_ant = self.lbl_query.text()
        
        if obj.objectName() == "le_labels" and evt.type() == QtCore.QEvent.FocusOut: 
            if (self.rb_all.isChecked() or self.rb_or.isChecked()) and self.le_labels.text() != "": 
                self.set_etiquetas()
  
        if obj.objectName() == "le_values" and evt.type() == QtCore.QEvent.FocusOut: 
            if (self.le_values.text()):
                self.lbl_query.setText(self.lbl_query.text() + self.le_values.text() + '}}')
            
        return False
       

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = VentanaPrincipal()
    window.boton_clear_query()
    window.show()
    sys.exit(app.exec_())
