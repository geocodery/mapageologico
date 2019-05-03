# -*- CODING: UTF-8 -*-

import sys
# from scripts.configs.settings import rutaX
# print rutaX().rutay('statics')

sys.path.insert(0, r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\scripts')
# sys.path.insert(0, r'D:\APPS\MAPA_GEOLOGICO\scripts')

from mapgeology import *
from metadata import *

arcpy.env.overwriteOutput = True


def decorator_loader(func):
    def decorator(*args):
        import subprocess
        import signal
        import os
        p = subprocess.Popen(r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\addin\Images\loader.exe')
        func(*args)
        os.kill(p.pid, signal.SIGTERM)
    return decorator
#
# @decorator_loader
# def contar():
#     import time
#     time.sleep(3)
class MainMapGeology:
    def __init__(self):
        self.hoja = arcpy.GetParameterAsText(0)
        self.zone = int(arcpy.GetParameterAsText(1))
        self.path = arcpy.GetParameterAsText(2)
        self.namehoja = u'{}'.format(arcpy.GetParameterAsText(3))
        self.sql = arcpy.GetParameterAsText(4)
        self.gdbold = Conexion().templateGDB

    def changeWorkspace(self):
        mxdold = arcpy.mapping.MapDocument(Template(self.zone).path)
        mxdold.saveACopy(self.path)
        del mxdold
        mxd = arcpy.mapping.MapDocument(self.path)
        mxd.replaceWorkspaces(self.gdbold, "FILEGDB_WORKSPACE", Conexion().conn, "FILEGDB_WORKSPACE", True)
        mxd.save()
        del mxd

    @decorator_loader
    def runProcess(self):
        self.changeWorkspace()
        classTableLegend = GenerateMap(self.hoja, self.sql, self.path, self.namehoja, self.zone)
        classTableLegend.main()
        classMetadata = MakeMetadata(self.path, self.hoja)
        classMetadata.main()

    def main(self):
        self.runProcess()


if __name__ == "__main__":
    poo = MainMapGeology()
    poo.main()
