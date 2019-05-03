# -*- CODING: UTF-8 -*-

import sys
#addin mainlegend
# from scripts.configs.model import GpoLegend, GplLegend, GlbLegend
# from scripts.legendProcess import Legend, Labels
#from scripts.configs.settings import rutaX

sys.path.insert(0, r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\scripts')
# sys.path.insert(0, r'D:\APPS\MAPA_GEOLOGICO\scripts')

from legendProcess import *
from annotationProcess import *
from functionGeneral import *


class MainLegend:
    def __init__(self):
        self.code = arcpy.GetParameterAsText(0)
        self.sql = arcpy.GetParameterAsText(1)

    def add_all_layers(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        gpo = GpoLegend().path
        gpl = GplLegend().path
        glb = GlbLegend()
        glb_mfl = arcpy.MakeFeatureLayer_management(glb.path, glb.namefc)
        for x in [gpo, gpl, glb.namefc]:
            self.add_layer_to_dataframe(x, mxd, df)

    def add_layer_to_dataframe(self, obj, mxd, df):
        lyr = arcpy.mapping.Layer(obj)
        lyr.definitionQuery = self.sql
        arcpy.mapping.AddLayer(df, lyr)
        arcpy.RefreshActiveView()

    def runProcess(self):
        classLegend = Legend(self.code, self.sql)
        classLegend.main()
        classAnnotation = Labels(self.code, self.sql)
        classAnnotation.main()

        self.add_all_layers()

    def main(self):
        try:
            self.runProcess()
        except Exception as e:
            raise RuntimeError(e)


if __name__ == "__main__":
    poo = MainLegend()
    poo.main()
