# -*- CODING: UTF-8 -*-

import sys
# from scripts.configs.settings import rutaX

#sys.path.insert(0, rutaX().rutay('scripts'))
sys.path.insert(0,r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\scripts')
#sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')
# sys.path.insert(0, r'D:\APPS\MAPA_GEOLOGICO\scripts')

from datationsFosil import *
from configs.nls import *


class MainTableData:
    def __init__(self):
        self.code = arcpy.GetParameterAsText(0)
        self.sql = arcpy.GetParameterAsText(1)
        self.zone = int(arcpy.GetParameterAsText(2))
        self.codhoja = FGeneral().codhoja
        self.fc = Dataciones(self.zone)
        self.feature = 'datacion'

    @property
    def validation_01(self):
        rows = [x[0] for x in arcpy.da.SearchCursor(self.fc.path, ["OID@"], self.sql)]
        if len(rows) > 0:
            return True
        else:
            return False

    def addFeatureToMap(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        gpl = GplDataciones().path
        glb = GlbDataciones()
        glb_mfl = arcpy.MakeFeatureLayer_management(glb.path, glb.namefc)
        for x in [gpl, glb.namefc]:
            self.add_layer_to_dataframe(x, mxd, df)

    def add_layer_to_dataframe(self, obj, mxd, df):
        lyr = arcpy.mapping.Layer(obj)
        lyr.definitionQuery = "{} = 'Head0' OR {}".format(self.codhoja, self.sql)
        arcpy.mapping.AddLayer(df, lyr)
        arcpy.RefreshActiveView()

    def runProcess(self):
        if self.validation_01:
            classTableLegend = MakeTables(self.code, self.sql, self.zone, self.feature)
            classTableLegend.main()
            self.addFeatureToMap()
        else:
            raise RuntimeError(nls().datacion().toolmsg_01)

    def main(self):
        self.runProcess()


if __name__ == "__main__":
    poo = MainTableData()
    poo.main()
