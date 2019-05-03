import arcpy
import os
from configs.config_symbol import *
from configs.model import *
from configs.statics import *
import json

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = 32718


class Symbol:
    def __init__(self, hoja, zone):
        self.hoja = hoja
        self.use = FeaturesUse(zone)
        self.tb = TbSimbolos()
        self.mea = MeasureSymbols()
        self.gptsimb = GptSimbolos()
        self.glbsimb = GlbSimbolos()
        self.gplsimb = GplSimbolos()
        self.gposimb = GpoSimbolos()
        self.gansimb = GanSimbolos()
        self.sql = "{} = '{}'".format(self.gposimb.codhoja, self.hoja)
        self.idx = 1
        self.containerPoint = []
        self.containerLine = []
        self.containerPolygon = []
        self.containerLabel = []
        self.JSON = jsonfiles()

    def getNumpyArray(self):
        self.npy = arcpy.da.FeatureClassToNumPyArray(self.tb.path, "*", None, None, False,
                                                     skip_nulls=False, null_value=-99999)

    def getCodeSymbol(self, idx):
        codes = self.npy[self.npy[self.tb.codcat] == str(idx)][self.tb.codi].tolist()
        return codes

    def createSqlClause(self, key, array):
        self.obj = self.use.items[key]
        self.fc = self.obj['fc']
        li = "({})".format(", ".join([str(x) for x in array]))
        sql = "{} = '{}' AND {} IN {}".format(self.fc.codhoja,
                                              self.hoja,
                                              self.fc.codi, li)
        return sql

    def getElmentSymbol(self, sql):
        clause = (None, "GROUP BY {}".format(self.fc.codi))
        elm = [x[0] for x in arcpy.da.SearchCursor(self.fc.path,
                                                   [self.fc.codi],
                                                   sql, None, False, clause)]
        return elm

    #etiquetas de simbologia
    def addLabels(self, key=None, codi=None):
        if codi:
            cdesc = self.mea.get_coordinates_decription(self.idx)
            lbl = self.npy[self.npy[self.tb.codi] == codi][self.tb.desc].tolist()[0]
            style = 2
        else:
            cdesc = self.mea.get_coordinates_title(self.idx)
            lbl = self.use.items[key]["name"]
            style = 1

        itemFeatures_sim = {
            "attributes": {self.glbsimb.nombre: lbl,
                           self.glbsimb.estilo: style,
                           self.glbsimb.hoja: self.hoja[:-1],
                           self.glbsimb.cuadrante: self.hoja[-1],
                           self.glbsimb.codhoja: self.hoja
                           },
            "geometry": cdesc
        }
        self.containerLabel.append(itemFeatures_sim)

    def makeSymbolPoint(self, key, array):
        # print array
        for x in array:
            csimb = self.mea.get_coordinates_point(self.idx)
            itemFeatures_sim = {
                "attributes": {self.gptsimb.codi: x,
                               self.gptsimb.hoja: self.hoja[:-1],
                               self.gptsimb.cuadrante: self.hoja[-1],
                               self.gptsimb.codhoja: self.hoja
                               },
                "geometry": csimb
            }
            self.containerPoint.append(itemFeatures_sim)
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            self.addLabels(codi=x)
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            self.idx = self.idx + 1

    def makeSymbolLine(self, key, array):
        for x in array:
            coords = self.mea.get_coordinates_line(self.idx)

            itemFeatures_gpl = {
                "attributes": {self.gplsimb.codi: x,
                               self.gplsimb.hoja: self.hoja[:-1],
                               self.gplsimb.cuadrante: self.hoja[-1],
                               self.gplsimb.codhoja: self.hoja
                               },
                "geometry": {"paths": [coords]}
            }
            self.containerLine.append(itemFeatures_gpl)
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            self.addLabels(codi=x)
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            self.idx = self.idx + 1


    def makeSymbolPolygon(self, key, array):
        for x in array:
            coords = self.mea.get_coordinates_polygon(self.idx)

            itemFeatures_gpo = {
                "attributes": {self.gposimb.codi: x,
                               self.gposimb.hoja: self.hoja[:-1],
                               self.gposimb.cuadrante: self.hoja[-1],
                               self.gposimb.codhoja: self.hoja
                               },
                "geometry": {"rings": [coords]}
            }

            self.containerPolygon.append(itemFeatures_gpo)
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            self.addLabels(codi=x)
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            self.idx = self.idx + 1


    def makeSymbol(self, key, array, geom):
        self.addLabels(key=key)
        self.idx = self.idx + 1

        if geom == 'gpt':
            self.makeSymbolPoint(key, array)
        elif geom == 'gpl':
            self.makeSymbolLine(key, array)
        elif geom == 'gpo':
            self.makeSymbolPolygon(key, array)

    def loadJson(self, geom, array):
        feature = {'gpl': self.JSON.gpl,
                   'gpt': self.JSON.gpt,
                   'gpo': self.JSON.gpoSimb,
                   'gptsimb': self.JSON.gptSimb}
        jsonOpen = open(feature[geom], "r")
        jsonLoad = json.load(jsonOpen)
        jsonOpen.close()
        jsonLoad["features"] = array
        json2shp = arcpy.AsShape(jsonLoad, True)
        return json2shp

    def delRows(self, feature):
        E = arcpy.da.Editor(Conexion().conn)
        E.startEditing(True, True)
        with arcpy.da.UpdateCursor(feature, ["OID@"], self.sql) as cursorUC:
            for x in cursorUC:
                cursorUC.deleteRow()
        del cursorUC
        E.stopEditing(True)

    def add_codhoja_annotation(self):
        rows = [x[0] for x in arcpy.da.SearchCursor(self.glbsimb.path, ["OID@"], self.sql)]
        sqlClause = "FeatureID IN ({})".format(", ".join([str(x) for x in rows]))
        E = arcpy.da.Editor(Conexion().conn)
        E.startEditing(True, True)
        with arcpy.da.UpdateCursor(self.gansimb.path,
                                   [self.gansimb.codhoja, self.gansimb.hoja, self.gansimb.cuadrante],
                                   sqlClause) as cursorUC:
            for x in cursorUC:
                x[0], x[1], x[2] = self.hoja, self.hoja[:-1], self.hoja[-1]
                cursorUC.updateRow(x)
        del cursorUC
        E.stopEditing(True)

    def process(self):
        self.getNumpyArray()
        for k, v in self.use.items.items():
            try:
                codes = self.getCodeSymbol(k)
                sql = self.createSqlClause(k, codes)
                elm = self.getElmentSymbol(sql)
                # pythonaddins.MessageBox(elm,'title')
                if len(elm) > 0:
                    self.makeSymbol(k, elm, self.obj["geom"])
            except:
                pass

        self.delRows(self.glbsimb.path)
        glb = self.loadJson("gpt", self.containerLabel)
        arcpy.Append_management(glb, self.glbsimb.path, "NO_TEST")

        self.delRows(self.gplsimb.path)
        gpl = self.loadJson("gpl", self.containerLine)
        arcpy.Append_management(gpl, self.gplsimb.path, "NO_TEST")

        self.delRows(self.gptsimb.path)
        gpt = self.loadJson("gptsimb", self.containerPoint)
        arcpy.Append_management(gpt, self.gptsimb.path, "NO_TEST")

        self.delRows(self.gposimb.path)
        gpo = self.loadJson("gpo", self.containerPolygon)
        arcpy.Append_management(gpo, self.gposimb.path, "NO_TEST")

        self.add_codhoja_annotation()

    def main(self):
        self.process()
