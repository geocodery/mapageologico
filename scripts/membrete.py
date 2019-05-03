#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainMapGeo import *


class fillText:
    def __init__(self, hoja, sql):
        self.elementText1 = TxMembrete().nombre
        self.elementText2 = TxFuenteDatos().nombre

        self.sql = "{} = '{}'".format(FGeneral().codhoja, hoja)
        self.membrete = [x for x in arcpy.da.SearchCursor(TbMetadata().tbMembrete, "*", sql)][0][1:10]
        self.fdatos = [x for x in arcpy.da.SearchCursor(TbMetadata().tbFDatos, "*", sql)][0][1:5]


    def main(self, mxd):
        text1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", self.elementText1)[0]
        text2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", self.elementText2)[0]

        text1.text = u'Presidente del Consejo Directivo: {} \nSecretaria General: {} \nCoordinador de Geología y Laboratorio de la PCD: {} \nAsesor de Investigación Geológica: {} \nDirectora de Geología Regional: {} \n \nBase Geológica 100k: {} \nAutor (es): {} \n \nDigitalización, SIG, edición: OSI - Cartografía Geológica Digital. \nEstandarización: {} \nReferencia geodésica: \nProyección Universal Transversal de Mercator (UTM) zona {}, \nDatum Sistema Geodésico Mundial 1984.'.format(
            self.membrete[0], self.membrete[1], self.membrete[2],
            self.membrete[3], self.membrete[4], self.membrete[5], self.membrete[6], self.membrete[7], MainMapGeology().zone)

        text2.text = u'Supervisión en campo: {} \nSupervisión digital: {} \nError de posicionamiento de GPS: {} metros. \nFormato de los datos: Geodatabase \nFecha de procesamiento de datos: {}'.format(
            self.fdatos[0], self.fdatos[1], self.fdatos[2], self.fdatos[3])

        arcpy.RefreshActiveView()
