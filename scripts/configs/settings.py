import os
#from nls import *
import json
#import pythonaddins

class rutaX: #RUTA A CAMBIAR PARA CORRER LOCAL O EN BD GEOCIENTIFICA
    def __init__(self):
        #self.rutax= r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico'
        self.rutax= r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico'

    def rutay(self,key):
        self.rutaf = os.path.join(self.rutax, key)
        return self.rutaf
class Statics:
    def __init__(self):
        #self.stat = r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\statics'
        self.stat= r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\statics'
        # self.stat = rutaX().rutay('statics')
        self.path = Conexion().path
        if os.path.exists(self.path):
            self.template = ReadJson(self.path, 'templates').read
        else:
            self.template = self.stat


class Conexion:
    def __init__(self):
        # self.templateGDB = rutaX().rutay('statics\MG_DGR_50K.gdb')
        self.templateGDB = 'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\statics\MG_DGR_50K.gdb'
        #self.templateGDB = r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\statics\MG_DGR_50K.gdb'
        self.gdbLocal = '22bbe73b-7793-4fcd-8a78-218d20c9894c'
        self.path = os.path.join('C:\{}'.format(self.gdbLocal), "{}.json".format(self.gdbLocal))
        if os.path.exists(self.path):
            self.conn = ReadJson(self.path, 'conn').read
        # self.bdgeocat = r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\connections\bdgeocat_publ_gis.sde'
        self.bdgeocat = r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\bdgeocientifica\datagis_ingemmet.gdb'

    @property
    def suma(self):
        return 5


class Services:
    def __init__(self):
        self.FEATURE_TO_POLYGON_SERVICE_TOOLBOX = "http://geocatmin.ingemmet.gob.pe:6080/arcgis/rest/services;GEOPROCESO/FeatureToPolygonService"
        self.FEATURE_VERTICES_TO_POINT_SERVICE_TOOLBOX = "http://geocatmin.ingemmet.gob.pe:6080/arcgis/rest/services;GEOPROCESO/FeatureVerticesToPointService"
        self.VIEWER_GEOLOGY_MAPS_100K_INGEMMET = "http://geocatminapp.ingemmet.gob.pe/complementos/Descargas/Mapas/publicaciones/serie_a/mapas"


class Tools:
    def __init__(self):
        self.TOOLS_GEOLOGY_MAPS = rutaX().rutay('tbx\CartografiaGeologica_DGR.tbx')
        #self.TOOLS_GEOLOGY_MAPS = r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\tbx\CartografiaGeologica_DGR.tbx'


class ReadJson:
    def __init__(self, path, key):
        self.path = path
        self.key = key

    @property
    def read(self):
        jsonfile = open(self.path, 'r')
        info = json.load(jsonfile)
        jsonfile.close()
        return info[self.key]


# conn = Conexion()
# conn.suma = 1
# print conn.suma


