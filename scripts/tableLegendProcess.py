import arcpy
import pythonaddins

from configs.model import *
from configs.nls import nls
import pandas as pd
import numpy as np

import uuid

arcpy.env.overwriteOutput = True


class TableLegend:
    def __init__(self, hoja, array, fields, sql):
        self.hoja = hoja
        self.array = array
        self.fields = fields
        self.sql = sql
        self.legend = tblegend()

    @property
    def getDataFrame(self):
        df = pd.DataFrame(self.array)
        return df

    def groupBy(self):
        df = self.getDataFrame
        gb = df.groupby(self.fields[1]).first().reset_index()#obtiene valores unicos
        self.npy = np.array(np.rec.fromrecords(gb.values))
        names = gb.dtypes.index.tolist()
        self.npy.dtype.names = tuple(names)

    def npy2table(self):
        self.tb = os.path.join(arcpy.env.workspace, 'tblegend')
        if arcpy.Exists(self.tb):
            arcpy.management.Delete(self.tb)
        arcpy.da.NumPyArrayToTable(self.npy, self.tb)

    def valid(self):
        valid= []
        m= None
        with arcpy.da.SearchCursor(self.legend.path, ['*'], self.sql) as cursorSC:
            for val in cursorSC:
                if val[4:-3].count(m) == len(val[4:-3]):
                    pass
                else:
                    valid.append(val[4:-3])
        # pythonaddins.MessageBox('{}-{}'.format(len(valid), valid), 'prueba')
        if len(valid) > 0:
            r = pythonaddins.MessageBox(nls().tablaLeyenda().valid, nls().tablaLeyenda().title, 4)
            if r == u"Yes":
                return True
            else:
                return False
        else:
            return True
        del cursorSC

    def delRows(self):
        if self.valid():
            with arcpy.da.UpdateCursor(self.legend.path, ['*'], self.sql) as cursorUC:
                for val in cursorUC:
                    cursorUC.deleteRow()
            return True
            del cursorUC

    def loadData(self):
        self.npy2table()
        if self.delRows():
            arcpy.Append_management(self.tb, self.legend.path, "NO_TEST")

    def viewTable(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        nameTb = os.path.basename(self.legend.path)
        tbLyr = arcpy.mapping.ListTableViews(mxd, nameTb, df)
        if len(tbLyr) > 0:
            tbview = tbLyr[0]
        else:
            tbview = arcpy.mapping.TableView(self.legend.path)
        tbview.definitionQuery = self.sql
        arcpy.mapping.AddTableView(df, tbview)
        arcpy.RefreshActiveView()
        del mxd

    def process(self):
        self.groupBy()
        #self.delRows()
        self.loadData()
        self.viewTable()

    def main(self):
        self.process()
