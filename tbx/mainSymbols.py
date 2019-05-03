# -*- CODING: UTF-8 -*-

import sys
# from scripts.configs.settings import rutaX

sys.path.insert(0, r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\scripts')
# sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')
# sys.path.insert(0, r'D:\APPS\MAPA_GEOLOGICO\scripts')

from symbols import *
from configs.nls import *


# def decorator_loader(func):
#     def decorator(*args):
#         import subprocess
#         import signal
#         import os
#         p = subprocess.Popen(r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\addin\Images\loader.exe')
#         func(*args)
#         os.kill(p.pid, signal.SIGTERM)
#     return decorator
#
# @decorator_loader
# def contar():
#     import time
#     time.sleep(3)


class MainSymbol:
    def __init__(self):
        self.hoja = arcpy.GetParameterAsText(0)
        self.zone = arcpy.GetParameterAsText(1)
        self.codhoja = FGeneral().codhoja
        self.sql1 = "{0} = 'Head0'".format(self.codhoja)
        self.sql2 = "{0} = 'Move'".format(self.codhoja)
        self.fields = ["CODI", "DESC", "HOJA", "CUADRANTE", "CODHOJA", "SHAPE@"]
        self.fieldsAn = ["ETIQUETA", "ESTILO", "HOJA", "CUADRANTE", "CODHOJA", "SHAPE@"]

    def addFeatureToMap(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]

        gpt = GptSimbolos().path
        gpl = GplSimbolos().path
        gpo = GpoSimbolos().path
        gan = GanSimbolos()

        with arcpy.da.UpdateCursor(gan.path,["HOJA", "CUADRANTE", "CODHOJA"],'"CODHOJA" IS NULL') as cursorU:
            for i in cursorU:
                i[0],i[1],i[2]= self.hoja[0:3],self.hoja[-1],self.hoja
                cursorU.updateRow(i)
        del cursorU

        gan_mfl = arcpy.MakeFeatureLayer_management(gan.path, gan.namefc)
        for x in [gpt, gpl, gpo, gan.namefc]:
            self.add_layer_to_dataframe(x, mxd, df)

    def add_layer_to_dataframe(self, obj, mxd, df):
        lyr = arcpy.mapping.Layer(obj)
        # lyr.definitionQuery = "{0} = 'Head0' OR {0} = '{1}'".format(self.codhoja, self.hoja)
        lyr.definitionQuery = "{0} = '{1}'".format(self.codhoja, self.hoja)
        arcpy.mapping.AddLayer(df, lyr)
        arcpy.RefreshActiveView()

    def fundicx(self):#funcion distancia de la coordenada inicial
        x = int([i[0] for i in arcpy.da.SearchCursor(GptSimbolos().path, "shape@x",self.sql1)][0])
        x2= (x-10375)/3250
        return int(x2)

    def runmovex(self,idx):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]

        gpt = GptSimbolos().path
        gpl = GplSimbolos().path
        gpo = GpoSimbolos().path
        gan = GlbSimbolos().path

        for x in [gpt, gpl, gpo, gan]:
            self.movex(x, mxd, df,idx)
    def movex(self,obj,mxd,df,idx):
        E = arcpy.da.Editor(Conexion().conn)
        E.startEditing(True, True)

        lyr = arcpy.mapping.Layer(obj)
        sql1 = self.sql1
        sql2 = self.sql2

        #INSERTAMOS LOS SIMBOLOS GEOGRAFICOS
        if "ESTILO" in [x.name for x in arcpy.ListFields(obj)]:
            fields = self.fieldsAn
            insert = arcpy.da.InsertCursor(lyr,fields)
        else:
            fields = self.fields
            insert = arcpy.da.InsertCursor(lyr,fields)


        with arcpy.da.SearchCursor(lyr,fields,sql1) as cursor:
            for i in cursor:
                a= 'Move'
                key = (i[0],i[1],i[2],i[3],a,i[5])
                insert.insertRow(key)
        del insert
        #UBICAMOS LOS SIMBOLOS GEOGRAFICOS A LA DERECHA Y ACTUALIZAMOS LOS CAMPOS
        with arcpy.da.UpdateCursor(lyr,["SHAPE@X","SHAPE@Y","HOJA", "CUADRANTE", "CODHOJA"],sql2) as cursorU:
            for i in cursorU:
                i[0]=i[0] + 3250*idx
                i[2],i[3],i[4]= self.hoja[0:3],self.hoja[-1],self.hoja
                cursorU.updateRow(i)
        del cursorU

        E.stopEditing(True)

    def runProcess(self):
        try:
            classSymbols = Symbol(self.hoja, int(self.zone))
            classSymbols.main()

            idx = (ceil((classSymbols.idx-1) / 15.0) -self.fundicx())
            self.runmovex(idx)


            self.addFeatureToMap()
        except Exception as e:
            raise RuntimeError(e)

    def main(self):
        self.runProcess()


if __name__ == "__main__":
    poo = MainSymbol()
    poo.main()
