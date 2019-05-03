from settings import *


class FGeneral:
    def __init__(self):
        self.codhoja = "CODHOJA"


class Datasets:
    def __init__(self, zone=None):
        self.dsSelect = {17: 5, 18: 6, 19: 7}
        self.dato_geog = "DS01_DATO_GEOGRAFICO"
        if zone:
            self.geologia = "DS0{}_GEOLOGIA_{}S".format(self.dsSelect[zone], zone)
        self.datacion = "DS09_DATACION"
        self.fosil = "DS10_FOSIL"
        self.leyenda = "DS11_LEYENDA"
        self.perfil = "DS12_PERFIL"
        self.simbolos = "DS13_SIMBOLOS"


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::: CAPAS GENERALES :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class GpoGeology:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codform = "CODIUNIHOJA" #CODFORM
        self.name = "ETIQUETA"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPO_DGR_ULITO_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# :::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::  TABLAS :::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class tblegend:
    def __init__(self):
        self.codi = "CODI"
        self.codform = "CODIUNIHOJA"#cambiar nombre codunihoja CODFORM
        self.name = "ETIQUETA"
        self.grupo = "GRUPO"
        self.formacion = "FORMACION"
        self.deposito = "DEPOSITO"
        self.miembro = "MIEMBRO"
        self.cvolc = "CVOLC"
        self.event = "EVENTO"
        self.batol = "BATOLIT"
        self.supuni = "SUP_UNIDAD"
        self.unidad = "UNIDAD"
        self.pluton = "PLUTON"
        self.descrip = "DESCRIP"
        self.serie = "SERIE"
        self.serie_adi = "SERIE_ADI"
        self.tipo = "TIPOFORM"
        self.contform = "CONTFORM"
        self.orden = "ORDEN"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nametb = "TB_MG_LEYENDA"
        self.nametb2 = "TB_MG_CODI"
        self.path = os.path.join(Conexion().conn, self.nametb)
        self.pathc= os.path.join(Conexion().conn, self.nametb2)


class tbage:
    def __init__(self):
        self.id_edad = "ID_EDAD"
        self.id_padre = "ID_PADRE"
        self.nombre = "NOMBRE"
        self.edad_ini = "EDAD_INI"
        self.ei_aprox = "EI_APROX"
        self.edad_fin = "EDAD_FIN"
        self.ef_aprox = "EF_APROX"
        self.nametb = "TB_MG_EDADES"
        self.path = os.path.join(Conexion().conn, 'TB_MG_EDADES')

#JORGE ADD
class tbcvolc:
    def __init__(self):
        self.id = "ID"
        self.nombre = "NOMBRE"
        self.path = os.path.join(Conexion().conn, 'TB_MG_CVOLC')


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::  FUENTES EXTERNAS  :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class GpoHojas100:
    def __init__(self):
        self.codhoja = "QDR_CODIGO_ALFANUMERICO"
        self.zonageo = "DOM_PROYECCION"
        self.nombreHoja = "QDR_NOMBRE"
        # self.nameDs = 'DATA_GIS.DS_PROYECTOS_INGEMMET'
        self.nameDs = 'DS_PROYECTOS_INGEMMET'
        # self.namefc = "DATA_GIS.GPO_HOJ_HOJAS_100"
        self.namefc = "GPO_HOJ_HOJAS_100"
        self.path = os.path.join(Conexion().bdgeocat, self.nameDs, self.namefc)


class GpoHojas50:
    def __init__(self):
        self.codhoja = "COD_CARTA"
        self.cuadrante = "CUADRANTE"
        # self.nameDs = 'DATA_GIS.DS_PROYECTOS_INGEMMET'
        self.nameDs = 'DS_PROYECTOS_INGEMMET'
        # self.namefc = "DATA_GIS.GPO_HOJ_HOJAS_50"
        self.namefc = "GPO_HOJ_HOJAS_50"
        self.path = os.path.join(Conexion().bdgeocat, self.nameDs, self.namefc)


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::  LEYENDA GEOLOGICA :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class GpoLegend:
    def __init__(self):
        self.codi = "CODI"
        self.codform = "CODFORM"
        self.name = "ETIQUETA"
        self.grupo = "GRUPO"
        self.formacion = "FORMACION"
        self.deposito = "DEPOSITO"
        self.miembro = "MIEMBRO"
        self.cvolc = "CVOLC"
        self.batol = "BATOLIT"
        self.supuni = "SUP_UNIDAD"
        self.unidad = "UNIDAD"
        self.pluton = "PLUTON"
        self.descrip = "DESCRIP"
        self.serie = "SERIE"
        self.serie_adi = "SERIE_ADI"
        self.tipo = "TIPOFORM"
        self.contform = "CONTFORM"
        self.orden = "ORDEN"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().leyenda
        self.namefc = "GPO_MG_FORM"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GplLegend:
    def __init__(self):
        self.codi = "CODI"
        self.orden = "ORDEN"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().leyenda
        self.namefc = "GPL_MG_CELD"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GptLegend:
    def __init__(self):
        self.nombre = "ETIQUETA"
        self.estilo = "ESTILO"
        # self.orden = "ORDEN"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().leyenda
        self.namefc = "GPT_MG_LABEL"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GlbLegend:
    def __init__(self):
        # self.orden = "ORDEN"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().leyenda
        self.namefc = "GAN_MG_LABEL"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# DATACIONES

class Dataciones:
    def __init__(self, zone):
        self.codi = "CODI"
        self.utm_e = "UTM_E"
        self.utm_n = "UTM_N"
        self.longitud = "LONGITUD"
        self.latitud = "LATITUD"
        self.altitud = "ALTITUD"
        self.zona = "ZONA"
        self.edad_ma = "EDAD_MA"
        self.error_ma = "ERROR_MA"
        self.metodo = "METODO"
        self.material = "MATERIAL"
        self.roca = "ROCA"
        self.unidad = "UNIDAD"
        self.muestra = "MUESTRA"
        self.referencia = "REFERENCIA"
        self.observaciones = "OBSERVACIONES"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPT_DGR_DATACI_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GplDataciones:
    def __init__(self):
        self.codi = "CODI"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().datacion
        self.namefc = "GPL_MG_CELD_DT"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GptDataciones:
    def __init__(self):
        self.nombre = "ETIQUETA"
        self.estilo = "ESTILO"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().datacion
        self.namefc = "GPT_MG_LABEL_DT"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GlbDataciones:
    def __init__(self):
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().datacion
        self.namefc = "GAN_MG_LABEL_DT"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# FOSILES

class Fosiles:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codi_muestra = "CODI_MUESTRA"
        self.codi_registro = "CODI_REGISTRO"
        self.fecha_colectado = "FECHA_COLECTADO"
        self.fecha_ingreso = "FECHA_INGRESO"
        self.localidad = "LOCALIDAD"
        self.distrito = "DISTRITO"
        self.provincia = "PROVINCIA"
        self.departamento = "DEPARTAMENTO"
        self.utm_n = "UTM_N"
        self.utm_e = "UTM_E"
        self.altitud = "ALTITUD"
        self.zona = "ZONA"
        self.latitud = "LATITUD"
        self.longitud = "LONGITUD"
        self.colectado_por = "COLECTADO_POR"
        self.institucion = "INSTITUCION"
        self.identificacion = "IDENTIFICACION"
        self.grupo_taxonomico = "GRUPO_TAXONOMICO"
        self.phyllum = "PHYLLUM"
        self.clase = "CLASE"
        self.orden = "ORDEN"
        self.superfamilia = "SUPERFAMILIA"
        self.familia = "FAMILIA"
        self.subfamilia = "SUBFAMILIA"
        self.genero = "GENERO"
        self.especie = "ESPECIE"
        self.descripcion = "DESCRIPCION"
        self.denominacion_anterior = "DENOMINACION_ANTERIOR"
        self.litologia = "LITOLOGIA"
        self.edad = "EDAD"
        self.unidad = "UNIDAD"
        self.cronoestratigrafia = "CRONOESTRATIGRAFIA"
        self.estado_conservacion = "ESTADO_CONSERVACION"
        self.paleoambiente = "PALEOAMBIENTE"
        self.zona_bioestratigrafica = "ZONA_BIOESTRATIGRAFICA"
        self.foto = "FOTO"
        self.descripcion_foto = "DESCRIPCION_FOTO"
        self.referencia = "REFERENCIA"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPT_DGR_FOSIL_{}S".format(zone)
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GplFosiles:
    def __init__(self):
        self.codi = "CODI"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().fosil
        self.namefc = "GPL_MG_CELD_FO"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GptFosiles:
    def __init__(self):
        self.nombre = "ETIQUETA"
        self.estilo = "ESTILO"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().fosil
        self.namefc = "GPT_MG_LABEL_FO"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GlbFosiles:
    def __init__(self):
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().fosil
        self.namefc = "GAN_MG_LABEL_FO"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::      SIMBOLOS      :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::

# Punto de observacion geologica - Punto
class Pog:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPT_DGR_POG_{}S".format(zone)
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Estructura volcanica - Punto
class GptVolcanico:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPT_DGR_ESVOLC_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Contacto geologico - Linea
class GplContactoGeologico:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_CONTAC_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Estructura volcanica - Linea
class GplVolcanico:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_ESVOLC_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Geomorfologia - Linea
class GplGeomorfologia:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_GEOFOR_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Secciones - Linea
class GplSeccion:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_SECCION_{}S".format(zone)
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Fallas - Linea
class GplFallas:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_FALLA_{}S".format(zone)
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Pliegues - Linea
class GplPliegues:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_PLIEG_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Dique - Linea
class GplDique:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPL_DGR_DIQUE_{}S".format(zone)
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Perfil y seccion
# ...


# Zona de alteracion - Poligono
class GpoAlteraciones:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPO_DGR_ALTERA_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Zona metamorfica - Poligono
class GpoMetamorfica:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPO_DGR_METAMO_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Geomorfologia - Poligono
class GpoGeomorfologia:
    def __init__(self, zone):
        self.codi = "CODI"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets(zone).geologia
        self.namefc = "GPO_DGR_GEOFOR_{}S".format(zone)#CAMBIO NOMBRE
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# Simbolos

class TbSimbolos:
    def __init__(self):
        self.codi = "CODI"
        self.codcat = "CODCAT"
        self.desc = "DESC"
        self.nametb = "TB_MG_DESC_SIMB"
        self.path = os.path.join(Conexion().conn, self.nametb)


class GlbSimbolos:
    def __init__(self):
        self.nombre = "ETIQUETA"
        self.estilo = "ESTILO"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().simbolos
        self.namefc = "GPT_MG_LABEL_SI"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GplSimbolos:
    def __init__(self):
        self.codi = "CODI"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().simbolos
        self.namefc = "GPL_MG_SIMB"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GptSimbolos:
    def __init__(self):
        self.codi = "CODI"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().simbolos
        self.namefc = "GPT_MG_SIMB"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GpoSimbolos:
    def __init__(self):
        self.codi = "CODI"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().simbolos
        self.namefc = "GPO_MG_SIMB"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GanSimbolos:
    def __init__(self):
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.nameDs = Datasets().simbolos
        self.namefc = "GAN_MG_LABEL_SI"
        self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::      TEXTOS      :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::

# Textos

class TxMembrete:
    def __init__(self):
        self.nombre = "7 MEMBRETE - TEXTO"


class TxFuenteDatos:
    def __init__(self):
        self.nombre = "6 FUENTE DE LOS DATOS - TEXTO"


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::      METADATOS      ::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::

# Metadatos - Tabla

class TbMetadata:
    def __init__(self):
        self.nombre = "NOMBRE"
        self.resumen = "RESUMEN"
        self.descripcion = "DESCRIPCION"
        self.autor = "AUTOR"
        self.creditos = "CREDITOS"
        self.tag = "TAG"
        self.enlace = "ENLACE"
        self.usos_lim = "USOS_LIM"
        self.hoja = "HOJA"
        self.cuadrante = "CUADRANTE"
        self.codhoja = "CODHOJA"
        self.namefc = "TB_MG_METADATA"

        self.membrete = "TB_MG_MEMBRETE"
        self.fdatos = "TB_MG_FDATOS"

        self.path = os.path.join(Conexion().conn, self.namefc)
        self.tbMembrete = os.path.join(Conexion().conn, self.membrete)
        self.tbFDatos = os.path.join(Conexion().conn, self.fdatos)
