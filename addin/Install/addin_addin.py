# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, r'D:\JORGE_YUPANQUI\Desarrollo\MapaGeologico\scripts')

# from scripts.configs.model import GpoHojas100
# from scripts.configs.settings import Services,rutaX
# from scripts.functionGeneral import functionCode


#sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')

#sys.path.insert(0, rutaX().rutay('scripts'))
# from configs.model import *
from configs.nls import *
from configs.statics import *
from functionGeneral import *
import arcpy
import pythonaddins
import string
import threading

arcpy.overwriteOutput = True
arcpy.ImportToolbox(Tools().TOOLS_GEOLOGY_MAPS)

#deberia salir2
class configGdb(object):
    """Implementation for addin_addin.conngdb (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False
        self.dirname = os.path.dirname(Conexion().path)#json
        self.connection = True if os.path.exists(Conexion().path) else False

    def onClick(self):
        ubi = pythonaddins.OpenDialog(nls().ConfigGDB().title, False, "#", nls().ConfigGDB().namebutton,lambda x:x,"Geodatabase (GDB)")
        if ubi:
            evalue = os.path.basename(ubi).split(".")
            if len(evalue) >= 2:
                if evalue[-1] == 'gdb':
                    if os.path.exists(self.dirname):
                        pass
                    else:
                        os.mkdir(self.dirname)
                    fl = Conexion().path
                    data = {'conn': ubi, 'templates': os.path.join(os.path.dirname(__file__), "templates")}
                    self.createJson(fl, data)
                    self.connection = True
                    pythonaddins.MessageBox(nls().suscefull, nls().title)
                else:
                    pythonaddins.MessageBox(nls().ConfigGDB().error, nls().titleError)
                    self.onClick()
            else:
                pythonaddins.MessageBox(nls().ConfigGDB().error, nls().titleError)
                self.onClick()
        else:
            pass

    def createJson(self, fl, data):
        with open(fl, 'w') as fp:
            json.dump(data, fp)


class selectRow(object):
    """Implementation for addin_addin.getRow (ComboBox)"""

    def __init__(self):
        self.editable = True
        self.enabled = True
        self.items = range(1, 38)
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = ""

    def onSelChange(self, selection):
        loadCode.disableLoad()

    def onEditChange(self, text):
        loadCode.disableLoad()

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


class selectCol(object):
    """Implementation for addin_addin.getCol (ComboBox)"""

    def __init__(self):
        self.editable = True
        self.enabled = True
        self.items = ",".join(string.ascii_uppercase).split(",")
        self.items.insert(14, u'Ñ')
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = ""

    def onSelChange(self, selection):
        loadCode.disableLoad()

    def onEditChange(self, text):
        loadCode.disableLoad()

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


class selectQuad(object):
    """Implementation for addin_addin.getQuad (ComboBox)"""

    def __init__(self):
        self.editable = True
        self.enabled = True
        self.items = range(1, 5)
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = ""

    def onSelChange(self, selection):
        loadCode.disableLoad()

    def onEditChange(self, text):
        loadCode.disableLoad()

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


class infoHoja(object):
    """Implementation for addin_addin.informacion (ComboBox)"""

    def __init__(self):
        self.editable = True
        self.enabled = False
        self.items = ""
        self.dropdownWidth = 'W' * 10
        self.width = 'W' * 10
        self.value = ""

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


class loadCode(object):
    """Implementation for addin_addin.loadCode (Button)"""

    def __init__(self):
        self.enabled = False
        self.checked = False
        self.codhoja = ""
        self.load = False
        self.tb = GpoHojas100()
        self.zone = None
        self.namehoja = None

    def onClick(self):
        # if conngdb.enabled == True:
        #     conngdb.enabled = False
        # else:
        #     conngdb.enabled = True
        v = self.getInfo
        if getRow.enabled:
            if v:
                getRow.enabled = False
                getCol.enabled = False
                getQuad.enabled = False
                conngdb.enabled = False
                fcode50 = functionCode(getRow.value,
                                       getCol.value,
                                       getQuad.value)
                self.codhoja = fcode50.makeCode
                self.codequery50 = fcode50.makeQuery()
                fcode100 = functionCode(getRow.value,
                                        getCol.value)
                self.codhoja100 = fcode100.makeCode
                self.load = True
                informacion.value = v
                informacion.refresh()
            else:
                pythonaddins.MessageBox(nls().loadCodeMSG().error,
                                        nls().titleError)
        else:
            r = pythonaddins.MessageBox(nls().changeCode(self.codhoja),
                                        nls().title, 4)
            if r == u"Yes":
                conngdb.enabled = True
                getRow.enabled = True
                getRow.value = ""
                getRow.refresh()
                getCol.enabled = True
                getCol.value = ""
                getCol.refresh()
                getQuad.enabled = True
                getQuad.value = ""
                getQuad.refresh()
                informacion.value = ""
                informacion.refresh()
                self.disableLoad()
                self.codhoja = ''
                self.codequery50 = ''
                self.codhoja100 = ''
                self.load = False

    def disableLoad(self):
        if getRow.value != "" and getCol.value != "" and getQuad.value != "":
            loadCode.enabled = True
        else:
            loadCode.enabled = False

    @property
    def getInfo(self):
        codesql = u"{} = '{}'".format(self.tb.codhoja,
                                      functionCode(getRow.value, getCol.value).makeCode)
        data = [[x[0], x[1]] for x in arcpy.da.SearchCursor(self.tb.path,
                                                            [self.tb.nombreHoja, self.tb.zonageo],
                                                            codesql)]
        if data == []:
            return False
        else:
            self.zone = data[0][1]
            self.namehoja = u'{}'.format(data[0][0])
            return u"  {} - {}S".format(data[0][0], data[0][1])


class makeTableLegend(object):
    """Implementation for addin_addin.TbLegend (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        res = pythonaddins.MessageBox(nls().tablaLeyenda().descrmb,
                                      nls().title, 1)
        if res == 'OK':
            poo = execute(self.runProcess)
            poo.onProcess()
        else:
            pass

    def runProcess(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = nls().tablaLeyenda().title
            dialog.description = nls().tablaLeyenda().descr
            dialog.animation = nls().tablaLeyenda().anima
            for x in xrange(10000):
                dialog.progress = x
                if x == 1:
                    arcpy.makeTableLegend(loadCode.codhoja,
                                          loadCode.zone)


class makeFeatureLegend(object):
    """Implementation for addin_addin.Legend (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        poo = execute(self.runProcess)
        poo.onProcess()

    def runProcess(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = nls().leyenda().title
            dialog.description = nls().leyenda().descr
            dialog.animation = nls().leyenda().anima
            for x in xrange(10000):
                dialog.progress = x
                if x == 1:
                    arcpy.makeLegend(loadCode.codhoja,          #row,col,quad
                                     loadCode.codequery50)      #"CODHOJA" = codhoja


class makeSimbolLegend(object):
    """Implementation for addin_addin.Simbolos (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        poo = execute(self.runProcess)
        poo.onProcess()

    def runProcess(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = nls().simbolos().title
            dialog.description = nls().simbolos().descr
            dialog.animation = nls().simbolos().anima
            for x in xrange(10000):
                dialog.progress = x
                if x == 1:
                    arcpy.makeSymbols(loadCode.codhoja,
                                      loadCode.zone)


class makeMap(object):
    """Implementation for addin_addin.MapGeo (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        if os.path.exists(Conexion().path):
            if loadCode.load:
                savepath = pythonaddins.SaveDialog(nls().mapGeo().titleDialog,
                                                   '{}.mxd'.format(loadCode.codhoja),"",lambda x: x,'Map Document(MXD)')
                if savepath:
                    evalue = os.path.basename(savepath).split(".")
                    if len(evalue) >= 2:
                        if evalue[-1] != "mxd":
                            pythonaddins.MessageBox(nls().mapGeo().errorFormat,
                                                    nls().titleError)
                    else:
                        savepath = '{}.mxd'.format(savepath)
                    try:
                        self.runProcess(savepath)
                        pythonaddins.MessageBox(nls().suscefull, nls().title)
                    except Exception as e:
                        pythonaddins.MessageBox(e, nls().titleError)
                else:
                    pass
            else:
                pythonaddins.MessageBox(nls().error, nls().titleError)
        else:
            pythonaddins.MessageBox(nls().failedConn, nls().titleError)

    def runProcess(self, savepath):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = nls().mapGeo().title
            dialog.description = nls().mapGeo().descr
            dialog.animation = nls().mapGeo().anima
            for x in xrange(10000):
                dialog.progress = x
                if x == 1:
                    arcpy.makeMapGeo(loadCode.codhoja,
                                     loadCode.zone,
                                     savepath,
                                     loadCode.namehoja,
                                     loadCode.codequery50)
                else:
                    pass


class makeProfile(object):
    """Implementation for addin_addin.Profile (Button)"""

    def __init__(self):
        self.enabled = False
        self.checked = False

    def onClick(self):
        pass


class makeTableData(object):
    """Implementation for addin_addin.Datacion (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        poo = execute(self.runProcess)
        poo.onProcess()

    def runProcess(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = nls().datacion().title
            dialog.description = nls().datacion().descr
            dialog.animation = nls().datacion().anima
            for x in xrange(10000):
                dialog.progress = x
                if x == 1:
                    arcpy.makeTableDatation(loadCode.codhoja,
                                            loadCode.codequery50,
                                            loadCode.zone)


class makeTableFosil(object):
    """Implementation for addin_addin.Fosil (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        poo = execute(self.runProcess)
        poo.onProcess()

    def runProcess(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = nls().fosil().title
            dialog.description = nls().fosil().descr
            dialog.animation = nls().fosil().anima
            for x in xrange(10000):
                dialog.progress = x
                if x == 1:
                    arcpy.makeTableFosil(loadCode.codhoja,
                                         loadCode.codequery50,
                                         loadCode.zone)


class execute(object):
    def __init__(self, function):
        self.function = function

    def onProcess(self):
        if os.path.exists(Conexion().path):
            if loadCode.load:
                try:
                    self.function()
                    pythonaddins.MessageBox(nls().suscefull, nls().title)
                except Exception as e:
                    pythonaddins.MessageBox(e, nls().titleError)
            else:
                pythonaddins.MessageBox(nls().error, nls().titleError)
        else:
            pythonaddins.MessageBox(nls().failedConn, nls().titleError)


class makeDecli(object):
    """Implementation for addin_addin.Declinacion (Button)"""

    def __init__(self):
        self.enabled = False
        self.checked = False

    def onClick(self):
        pass


class guideUser(object):
    """Implementation for addin_addin.guide (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False
        self.path = Template().guideuser
        self.path2 = Template().mElabor

    def onClick(self):
        if os.path.exists(self.path):
            openFiles(self.path).process()
            openFiles(self.path2).process()
        else:
            pythonaddins.MessageBox(nls().guideUser().msg, nls().title)


class openWs(object):
    """Implementation for addin_addin.workspace (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        if os.path.exists(Conexion().path):
            path = os.path.dirname(Conexion().conn)
            openFiles(path).process()
        else:
            pythonaddins.MessageBox(nls().failedConn, nls().titleError)


class viewHoja(object):
    """Implementation for addin_addin.viewHoja (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False
        self.url = Services().VIEWER_GEOLOGY_MAPS_100K_INGEMMET

    def onClick(self):
        if loadCode.load:
            hoja100 = loadCode.codhoja100
            path = self.url + '/{}.htm'.format(hoja100)
            openFiles(path).process()
        else:
            pythonaddins.MessageBox(nls().error, nls().titleError)


class openFiles(object):
    def __init__(self, parameter):
        self.parameter = parameter

    def process(self):
        t = threading.Thread(target=os.startfile, args=(self.parameter,))
        t.start()
        t.join()

