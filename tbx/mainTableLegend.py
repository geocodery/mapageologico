# -*- CODING: UTF-8 -*-

import sys
import pythonaddins
# from scripts.configs.settings import rutaX

# sys.path.insert(0, rutaX('scripts').path)
sys.path.insert(0,r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\scripts')
#sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')

from configs.nls import *
from tableLegendProcess import *
from configs.config_tblegend import *


class MainTableLegend:
    def __init__(self):
        self.hoja = arcpy.GetParameterAsText(0)
        self.zone = int(arcpy.GetParameterAsText(1))
        self.codhoja = FGeneral().codhoja
        self.gpoGeology = GpoGeology(self.zone)
        self.sql = "{} = '{}'".format(self.codhoja, self.hoja)
        self.fields = FieldsUse().fields

    def _validation01(self):
        self.npy = arcpy.da.FeatureClassToNumPyArray(self.gpoGeology.path, self.fields,
                                                     self.sql, None, False,
                                                     skip_nulls=False,
                                                     null_value=-99999)

    def process(self):
        self._validation01()
        if self.npy.size > 0:
            classTableLegend = TableLegend(self.hoja, self.npy, self.fields, self.sql)
            classTableLegend.main()
        else:
            raise RuntimeError(nls().tablaLeyenda().toolmsg_01)

    def main(self):
        self.process()


if __name__ == "__main__":
    poo = MainTableLegend()
    poo.main()
