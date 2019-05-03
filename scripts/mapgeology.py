#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
import json
import qrcode
from configs.model import *
from configs.statics import *
from functionGeneral import *
from membrete import fillText
import pythonaddins


arcpy.env.overwriteOutput = True


class GenerateMap:
    def __init__(self, hoja, sql, pathmxd, namehoja, zone):
        self.pathmxd = pathmxd
        self.hoja = hoja
        self.hoja100 = functionCode()._codeTransform(self.hoja, of=50)
        self.sql = sql
        self.sql100 = "{} = '{}'".format(GpoHojas100().codhoja,
                                         self.hoja100)  # MODIFICAR EN CASO EL IDENTIFICADOR VARIE
        self.sql50 = "{} = '{}' AND {} = {}".format(GpoHojas50().codhoja, self.hoja100, GpoHojas50().cuadrante,
                                                    self.hoja[-1])  # MODIFICAR EN CASO EL IDENTIFICADOR VARIE
        self.nombrehoja = namehoja
        self.zone = zone
        self.temp = Template()  # Statics.py
        self.mxd = arcpy.mapping.MapDocument(pathmxd)
        self.outqr = self.temp.outqr
        self.dfs = Componentes()  # Statics.py
        self.principal = self.dfs.Principal(self.zone)  # Statics.py
        self.leyenda = self.dfs.Leyenda()  # Statics.py
        self.caratula = self.dfs.Caratula()  # Statics.py
        # self.ubiReg = self.dfs.UbiRegional()  # Statics.py
        self.perfil = self.dfs.Perfil()  # Statics.py
        self.ubiCuad = self.dfs.UbiCuadrante()  # Statics.py
        self.elem = Elements()  # Statics.py
        self.dataciones = self.dfs.Dataciones()  # Statics.py
        self.fosiles = self.dfs.Fosiles()  # Statics.py
        self.simbolos = self.dfs.Simbolos()  # Statics.py

        # with open(r'', 'w') as f:
        #     f.write()
        self.coordSys = CoordSystem()


    def runQuery(self, objDf, nameLyr=None, lyrExtent=None, scale=None, table=None):
        df = arcpy.mapping.ListDataFrames(self.mxd, objDf.name)[0]
        lyrs = {x.name: x for x in arcpy.mapping.ListLayers(self.mxd, nameLyr, df)}
        for k, v in lyrs.items():
            if v.supports("DEFINITIONQUERY"):
                #en caso de usar todas las curvas
                if "OCEANO" not in k:
                    v.definitionQuery = "CODHOJA = 'Head0' OR {}".format(self.sql) if table else self.sql

                #en caso de solo usar curvas maestras
        #         if "CURVAS" in k:
        #             v.definitionQuery = "RASGO_SECU='Índice' AND {}".format(self.sql)
        #
        #         else:
        #             v.definitionQuery = "CODHOJA = 'Head0' OR {}".format(self.sql) if table else self.sql
        # arcpy.RefreshActiveView()
        if lyrExtent:
            self.extentDataFrame(df, lyrs[lyrExtent], scale)
        arcpy.RefreshActiveView()

    def extentDataFrame(self, objDf, objlyr, scale=None):

        objDf.extent = objlyr.getSelectedExtent()

        if scale:
            if scale == "df":
                newextent = objDf.extent
                newextent.YMax = newextent.YMax + 1000
                objDf.extent = newextent

                # objDf.scale = 45000
            else:
                objDf.scale = scale
        arcpy.RefreshActiveView()


    def sheetCurrent(self, objDf, nameLyr, nameLyr2):
        df = arcpy.mapping.ListDataFrames(self.mxd, objDf.name)[0]
        lyr = arcpy.mapping.ListLayers(self.mxd, nameLyr, df)[0]
        lyr.definitionQuery = self.sql50

        lyr2 = arcpy.mapping.ListLayers(self.mxd, nameLyr2, df)[0]
        lyr2.definitionQuery = self.sql50

        arcpy.RefreshActiveView()

    # CREACION DE CODIGO QR
    @property
    def createQrCode(self):
        pathQr = os.path.join(self.outqr, "{}.png".format(self.hoja))
        img = qrcode.make(self.hoja)
        fileqr = open(pathQr, "wb")
        img.save(fileqr)
        fileqr.close()
        return pathQr

    def addQrToMap(self):

        nameElement = QrCode().element
        element = arcpy.mapping.ListLayoutElements(self.mxd, "PICTURE_ELEMENT", nameElement)[0]
        element.sourceImage = self.createQrCode
        arcpy.RefreshActiveView()

    def ubiCuadrante(self):
        containerSentence = []
        value = self.hoja100[-1]
        row = self.hoja100.split("-")[0]
        filas = [str(int(row) - 1), row, str(int(row) + 1)]
        key = [k for k, v in self.ubiCuad.alpha.items() if v == value][0]
        idxR = self.ubiCuad.alpha[key + 1] if self.ubiCuad.alpha.has_key(key + 1) else None
        idxL = self.ubiCuad.alpha[key - 1] if self.ubiCuad.alpha.has_key(key - 1) else None
        columnas = [idxL, value, idxR]
        for x in filas:
            for m in columnas:
                if m:
                    sentence = "{} = '{}-{}'".format(GpoHojas100().codhoja, x, m)
                    containerSentence.append(sentence)

        df = arcpy.mapping.ListDataFrames(self.mxd, self.ubiCuad.name)[0]
        lyr = arcpy.mapping.ListLayers(self.mxd, self.ubiCuad.HojasPeru, df)[0]
        lyr.definitionQuery = " OR ".join(containerSentence)
        df.extent = lyr.getSelectedExtent()
        df.scale = self.ubiCuad.scale

        lyrs50 = arcpy.mapping.ListLayers(self.mxd, self.ubiCuad.hojaCuad, df)[0]
        lyrs50.definitionQuery = "{} = '{}'".format(GpoHojas50().codhoja, self.hoja100)

        lyrUpd50 = arcpy.mapping.ListLayers(self.mxd, self.ubiCuad.hojaActual, df)[0]
        lyrUpd50.definitionQuery = self.sql50
        arcpy.RefreshActiveView()

    def updateLabels(self):
        labels = arcpy.mapping.ListLayoutElements(self.mxd, self.elem.datahoja["tipo"], self.elem.datahoja["nombre"])
        cambio = u"{} - HOJA {}".format(self.nombrehoja.upper(), self.hoja.upper())

        for x in labels:
            # x.text = u"{} - HOJA {}".format(self.nombrehoja.upper(), self.hoja.upper())
            x.text = x.text.replace(u'{$NOMBRE} - HOJA {$HOJA}',cambio)
        # label1 = arcpy.mapping.ListLayoutElements(self.mxd, self.elem.datahoja["tipo"], "DATAHOJA1")[0]
        # label1.text = label1.text.replace(u'{$NOMBRE} - HOJA {$HOJA}',cambio)

        fillText(self.hoja, sql=self.sql).main(self.mxd)
        arcpy.RefreshActiveView()


    # EXPORTAR MAPA EN FORMATO MXD
    def saveMxd(self):
        self.mxd.save()
        del self.mxd

    def main(self):
        self.runQuery(self.principal, nameLyr=None, lyrExtent=self.principal.extentDf,
                      scale=self.principal.scale)  # PRINCIPAL
        self.runQuery(self.leyenda, nameLyr=None, lyrExtent=self.leyenda.extentDf)  # LEYENDA
        self.runQuery(self.perfil, nameLyr=None, lyrExtent=self.perfil.extentDf, scale=self.perfil.scale) # PERFIL
        self.runQuery(self.dataciones, nameLyr=None, lyrExtent=None, scale=None, table=True)  # DATACIONES
        self.runQuery(self.fosiles, nameLyr=None, lyrExtent=None, scale=None, table=True)  # DATACIONES
        self.runQuery(self.simbolos, nameLyr=None, lyrExtent=self.simbolos.extentDf, scale=self.simbolos.scale) # SIMBOLOS
        self.sheetCurrent(self.caratula, self.caratula.hojaActual, self.caratula.pathArrow) # CARATULA
        # self.ubiRegional()
        self.ubiCuadrante()
        self.updateLabels()
        self.addQrToMap()
        self.saveMxd()



# foo = GenerateMap('29v2', "CODHOJA = '29v2'", r'D:\JORGE_YUPANQUI\INGEMMET\MAPAS 2017\MXD\19S\test.mxd', 'paquita', 19)
# foo.main()