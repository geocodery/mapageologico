# -*- coding: utf-8 -*-

class nls:
    def __init__(self):
        self.title = u"© 2017 Ingemmet - OSI"
        self.titleError = u'{} | Error'.format(self.title)  # ERROR
        self.error = u"Debe seleccionar un código de hoja \nantes de realizar la operación."  # ERROR
        self.suscefull = u"El proceso se realizó con éxito"
        self.failedConn = u'No ha configurado la ubicación de la geodatabase plantilla'  # ERROR

    def changeCode(self, code):
        msg = u"Desea terminar el proyecto \n en la hoja {}".format(code)
        return msg

    class datacion:
        def __init__(self):
            self.title = "Tabla de dataciones"
            self.descr = "Generando Tabla de Dataciones..."
            self.anima = "File"
            self.toolmsg_01 = "La hoja consultada no contiene registros."  # ERROR

    class fosil:
        def __init__(self):
            self.title = u"Tabla de Fósiles"
            self.descr = u"Generando tabla de Fósiles..."
            self.anima = "File"
            self.toolmsg_01 = "La hoja consultada no contiene registros."  # ERROR

    class loadCodeMSG:
        def __init__(self):
            self.error = u"El código de hoja ingresado no existe"  # ERROR

    class ConfigGDB:
        def __init__(self):
            self.title = "Seleccionar Template GDB (Plantilla de Geodatabase)"
            self.namebutton = "Cargar"
            self.error = "El archivo seleccionado no es una Geodatabase [formato invalido]."  # ERROR

    class simbolos:
        def __init__(self):
            self.title = u"Símbolos"
            self.descr = u"Generando Cuadro de símbolos..."
            self.anima = "File"

    class tablaLeyenda:
        def __init__(self):
            self.descrmb = u"¿Desea modificar los valores en TB_MG_LEYENDA de la hoja seleccionada?"
            self.valid = u"Ya existen datos establecidos en la hoja seleccionada, ¿desea borrarlos?"
            self.title = u"Tabla Leyenda"
            self.descr = u"Generando tabla estandarizada para construcción\nde leyenda..."
            self.anima = "File"
            self.toolmsg_01 = u'No existe información de la hoja indicada'  # ERROR

    class leyenda:
        def __init__(self):
            self.title = u"Leyenda Geológica"
            self.descr = u"Al finalizar la operación considerar su verificación y personalización."
            self.anima = "File"

    class mapGeo:
        def __init__(self):
            self.titleDialog = u"Establecer direción de almacenamiento del proyecto .mxd"
            self.title = u"Mapa Geológico"
            self.descr = u"Generando Mapa Geológico 1:50000"
            self.anima = u"File"
            self.errorFormat = u"El nombre ingresado no pertenece a un proyecto .mxd"  # ERROR
            self.error = u"Error al crear el proyecto .mxd"  # ERROR

    class guideUser:
        def __init__(self):
            self.msg = u"Guía de usuario en elaboración"
