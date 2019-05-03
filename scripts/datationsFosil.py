# -*- coding: utf-8 -*-
import arcpy
import os
from configs.measure_tables import *
from configs.model import *
from configs.statics import *
import json

arcpy.env.overwriteOutput = True


class MakeTables:
    def __init__(self, hoja, sql, zone, featureSelect):
        self.hoja = hoja
        self.featureSelect = featureSelect
        self.classTable = MeasureTables(featureSelect)  # measure_table
        self.cols = self.classTable.head
        self.fc = Dataciones(zone) if featureSelect == 'datacion' else Fosiles(zone)
        self.GplFc = GplDataciones() if featureSelect == 'datacion' else GplFosiles()
        self.GptFc = GptDataciones() if featureSelect == 'datacion' else GptFosiles()
        self.GblFc = GlbDataciones() if featureSelect == 'datacion' else GlbFosiles()
        self.fcpath = self.fc.path
        self.sql = sql
        self.JSON = jsonfiles()

    def delRows(self, geom):
        feature = {"gpt": self.GptFc.path, "gpl": self.GplFc.path}
        E = arcpy.da.Editor(Conexion().conn)
        E.startEditing(True, True)
        with arcpy.da.UpdateCursor(feature[geom], ["OID@"], self.sql) as cursorUC:
            for x in cursorUC:
                cursorUC.deleteRow()
        del cursorUC
        E.stopEditing(True)

    def loadJson(self, geom, array):
        feature = {'gpl': self.JSON.gpl, 'gpt': self.JSON.gpt}
        jsonOpen = open(feature[geom], "r")
        jsonLoad = json.load(jsonOpen)
        jsonOpen.close()
        jsonLoad["features"] = array
        json2shp = arcpy.AsShape(jsonLoad, True)
        return json2shp

    def getCellRows(self, array):
        container_gpl, container_gpt = [], []
        row = 0
        for r in array:
            row = row + 1
            col = 0
            for c in r:
                col = col + 1

                # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                cen = self.classTable.get_center_coordinate_cell(col, row)
                itemFeatures_gpt = {
                    "attributes": {self.GptFc.nombre: "" if c in (-99999, "-99999") else c,
                                   self.GptFc.estilo: 2,
                                   self.GptFc.hoja: self.hoja[:-1],
                                   self.GptFc.cuadrante: self.hoja[-1],
                                   self.GptFc.codhoja: self.hoja
                                   },
                    "geometry": cen
                }
                container_gpt.append(itemFeatures_gpt)

                # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                coords = self.classTable.get_cell_coordinates(col, row)

                itemFeatures_gpl = {
                    "attributes": {self.GplFc.codi: 1,
                                   self.GplFc.hoja: self.hoja[:-1],
                                   self.GplFc.cuadrante: self.hoja[-1],
                                   self.GplFc.codhoja: self.hoja
                                   },
                    "geometry": {"paths": [coords]}
                }
                container_gpl.append(itemFeatures_gpl)

        return [container_gpl, container_gpt]

    def add_codhoja_annotation(self):
        rows = [x[0] for x in arcpy.da.SearchCursor(self.GptFc.path, ["OID@"], self.sql)]
        sqlClause = "FeatureID IN ({})".format(", ".join([str(x) for x in rows]))
        E = arcpy.da.Editor(Conexion().conn)
        E.startEditing(True, True)
        with arcpy.da.UpdateCursor(self.GblFc.path,
                                   [self.GblFc.codhoja, self.GblFc.hoja, self.GblFc.cuadrante],
                                   sqlClause) as cursorUC:
            for x in cursorUC:
                x[0], x[1], x[2] = self.hoja, self.hoja[:-1], self.hoja[-1]
                cursorUC.updateRow(x)
        del cursorUC
        E.stopEditing(True)

    def makeTable(self):
        col, row = 0, 0
        fields = [v['name'] for k, v in self.cols.items()]

        npy = arcpy.da.FeatureClassToNumPyArray(self.fcpath, fields,
                                                self.sql, None, False,
                                                skip_nulls=False,
                                                null_value=-99999)

        container = self.getCellRows(npy)
        json2shp_gpl = self.loadJson('gpl', container[0])
        json2shp_gpt = self.loadJson('gpt', container[1])
        self.delRows('gpl')
        self.delRows('gpt')
        arcpy.Append_management(json2shp_gpl, self.GplFc.path, "NO_TEST")
        arcpy.Append_management(json2shp_gpt, self.GptFc.path, "NO_TEST")
        self.add_codhoja_annotation()

    def main(self):
        self.makeTable()
