import pythonaddins

from settings import *
import string



class Template:
    def __init__(self, zona=None):
        if zona:
            self.path = os.path.join(Statics().template, 'template{}s_v103.mxd'.format(zona))
        self.outqr = os.path.join(Statics().stat, 'qrcode')
        self.outxml = os.path.join(Statics().stat, 'xml')
        self.translator = os.path.join(Statics().stat, 'translator')
        self.guideuser = os.path.join(Statics().stat, 'docs', 'MG50K_GuiaUsuario.pdf')
        self.mElabor = os.path.join(Statics().stat, 'docs', 'M_Elaboracion_50k.pdf')


class Translators:
    def __init__(self):
        self.TR01 = os.path.join(Template().translator, 'ARCGIS2FGDC.xml')
        self.xmltempl = os.path.join(Template().translator, 'template.xml')



class Componentes:
    class Principal:
        def __init__(self, zone):
            self.sel = {
                17: 5,
                18: 6,
                19: 7
            }
            self.name = "1 MAPA PRINCIPAL"
            self.gptVolc = "GPT_DS0{}_Volcanico".format(self.sel[zone])
            self.gptPog = "GPT_DS0{}_Pog".format(self.sel[zone])
            self.gpoGeo = "GPT_DS0{}_Fosil".format(self.sel[zone])
            self.gptData = "GPT_DS0{}_Datacion".format(self.sel[zone])
            self.gplVolc = "GPL_DS0{}_Volcanico".format(self.sel[zone])
            self.gplSecc = "GPL_DS0{}_Seccion".format(self.sel[zone])
            self.gplPli = "GPL_DS0{}_Pliegue".format(self.sel[zone])
            self.gplgeom = "GPL_DS0{}_Geomorfologia".format(self.sel[zone])
            self.gplGeo = "GPL_DS0{}_Geologia".format(self.sel[zone])
            self.gplFall = "GPL_DS0{}_Fallas".format(self.sel[zone])
            self.gplDique = "GPL_DS0{}_Dique".format(self.sel[zone])
            self.gpoGeom = "GPO_DS0{}_Geomorfologia".format(self.sel[zone])
            self.gpoAlt = "GPO_DS0{}_Alteraciones".format(self.sel[zone])
            self.gpoMeta = "GPO_DS0{}_Metamorfico".format(self.sel[zone])
            self.gpoGeo = "GPO_DS0{}_Geologia".format(self.sel[zone])

        @property
        def extentDf(self):
            return self.gpoGeo

        @property
        def scale(self):
            sc = 50000
            return sc

    class Leyenda:
        def __init__(self):
            self.name = "2 LEYENDA"
            self.glb = "GAN_DS11_Etiquetas"
            self.gpl = "GPL_DS11_Celdas"
            self.gpo = "GPO_DS11_Formaciones"

        @property
        def extentDf(self):
            return self.gpl

    class Fosiles:
        def __init__(self):
            self.name = "3 FOSILES"
            self.glb = "GAN_DS10_Anotaciones"
            self.gplFosil = "GPL_DS10_Fosil"

        @property
        def extentDf(self):
            return self.gplFosil

    class Dataciones:
        def __init__(self):
            self.name = "4 DATACIONES"
            self.glb = "GAN_DS09_Anotaciones"
            self.gplData = "GPL_DS09_Datacion"

        @property
        def extentDf(self):
            return self.gplData

    class Simbolos(object):
        def __init__(self):
            self.name = "5 SIMBOLOS"
            self.glb = "GAN_DS13_Anotaciones"
            self.gpt = "GPT_DS13_Simbolos"
            self.gpl = "GPL_DS13_Simbolos"
            self.gpo = "GPO_DS13_Simbolos"

        @property
        def extentDf(self):
            # return self.gpt
            return self.glb

        @property
        def scale(self):
            sc = 50000
            return sc

    # class UbiRegional:
    #     def __init__(self):
    #         self.name = "6 MAPA DE UBICACION REGIONAL"
    #         self.hojaActual = "GPO_HojaActual_50k"
    #         self.hojasPeru = "GPO_HojasPeru_100k"
    #
    #     @property
    #     def scale(self):
    #         sc = 2500000
    #         return sc


    class FuenteDatos:
        def __init__(self):
            self.name = "6 FUENTE DE LOS DATOS"
            self.tb = "TB_MG_FUENTE_DATOS"

    class Membrete:
        def __init__(self):
            self.name = "7 MEMBRETE"
            self.tb = "TB_MG_MEMBRETE"

    class Caratula:
        def __init__(self):
            self.name = "8 CARATULA"
            self.limites = "GPO_Departamentos"
            self.hojaActual = "GPO_HojaActual_50k"
            self.lago = "GPO_DS01_LagoTiticaca"
            self.pathArrow = "GPO_DGR_ARROW"

            # self.P1x = -80.1781
            # self.P1y = -13.2282
            # self.P2x = -79.7283
            # self.P2y = -13.5709
            #
            # self.pathArrow = os.path.join(Conexion().conn, 'GPO_DGR_ARROW')
            # self.lyrArrow = os.path.join(Statics().stat, 'lyr\Arrow.lyr')

    class UbiCuadrante:
        def __init__(self):
            self.name = "9 UBICACION DE CUADRANTE"
            self.hojaCuad = "GPO_HojasCuad_50k"
            self.hojaActual = "GPO_HojaActual_50k"
            self.HojasPeru = "GPO_HojasPeru_100k"
            alphaTmp = ",".join(string.ascii_lowercase).split(",")
            alphaTmp.insert(14, '\xd1')
            self.alpha = {k: x.lower() for k, x in enumerate(alphaTmp)}

        @property
        def scale(self):
            sc = 3500000
            return sc

    class Perfil:
        def __init__(self):
            self.name = "10 PERFIL Y SECCION GEOLOGICA"
            self.glb = "GAN_DS12_Anotaciones"
            self.gpl = "GPL_DS12_Celdas"
            self.gpo = "GPO_DS12_Formaciones"

        @property
        def extentDf(self):
            return self.gpl

        @property
        def scale(self):
            # sc = 44000
            sc = "df"
            return sc

    class DecMagnetica:
        def __init__(self):
            self.name = "11 DECLINACION MAGNETICA"


class QrCode:
    def __init__(self):
        self.x = 84
        self.y = 7
        self.heigth = 4
        self.width = 4
        self.element = "QRCODE"


class Scale:
    def __init__(self):
        self.mp = 50000
        self.lg = 50000


class Elements:
    def __init__(self):
        self.datahoja = {
            "nombre": "DATAHOJA",
            "tipo": "TEXT_ELEMENT"
        }


class CoordSystem:
    def __init__(self):
        self.utm17s = 32717
        self.utm18s = 32718
        self.utm19s = 32719
        self.wgs84 = 4326


class jsonfiles:
    def __init__(self):
        self.gpl = os.path.join(Statics().stat, 'json\linea.json')
        self.gpo = os.path.join(Statics().stat, 'json\leyendaPoligono.json')
        self.gpt = os.path.join(Statics().stat, 'json\punto.json')
        self.gptSimb = os.path.join(Statics().stat, 'json\simbolosPunto.json')
        self.gpoSimb = os.path.join(Statics().stat, 'json\simbolosPoligono.json')


class Annotation:
    def __init__(self):
        self.head_age_label = {
            1: "ERATEMA",
            2: "SISTEMA",
            3: "SERIE",
            4: "EDAD (MA)"
        }
        self.head_column_label = {
            1: u"UNIDADES LITOESTRATIGRAFICAS",
            2: u"MORFOESTRUCTURAS VOLCANICAS",
            3: u"ROCAS INTRUSIVAS Y SUBVOLCANICAS"
        }
        self.headClass = {
            "ages": 1,
            "colum": 2
        }
        self.laterClass = {
            "eratema": 3,
            "sistema": 4,
            "serie": 5,
            "edad": 6
        }
        self.annotationClass = {
            "descripcion": 7,
            "grupo": 8,
            "formacion_deposito": 9,
            "miembro": 10,
            "conjunto_volcanico": 11,
            "batolito": 12,
            "super_unidad": 13,
            "unidad": 14,
            "pluton": 15
        }


