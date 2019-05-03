## -*- coding: utf-8 -*-


import arcpy
import json
import pandas as pd
from configs.model import *
from configs.measure import *
from configs.statics import *
from annotationProcess import *


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = 32718

xyini = [10000, 10000]


class Legend:
    def __init__(self, hoja, sql):
        self.hoja = hoja
        self.hoja100 = hoja[:-1]
        self.cuadrante = hoja[-1]
        self.sql = sql
        self.x, self.y = xyini[0], xyini[1]  # MODIFICA LA POSICION DONDE SE CREARA LA LEYENDA
        self.lg = tblegend()
        self.cd = tblegend()
        self.cvt = tbcvolc()
        self.ed = tbage()  # MODULE: configs | file: model
        self.GPOLeyend = GpoLegend()  # model.py
        self.GPLLeyend = GplLegend()  # model.py
        self.GPTLeyend = GptLegend()  # model.py
        self.edad = ColumAge(self.x, self.y)  # MODULE: configs | file: measure
        self.jsonfiles = jsonfiles()  # MODULE: configs | file: statics
        self.containerLines = []

    # ETAPA INICIAL
    # PREPARACION DE INFORMACION


    def dfpandas(self):
        lg = arcpy.da.TableToNumPyArray(self.lg.path, ["*"], self.sql, skip_nulls=False, null_value=-99999)
        cd = arcpy.da.TableToNumPyArray(self.cd.pathc, ["*"], None, skip_nulls=False, null_value=-99999)
        ed = arcpy.da.TableToNumPyArray(self.ed.path, ["*"], None, skip_nulls=False, null_value=-99999)
        cv = arcpy.da.TableToNumPyArray(self.cvt.path, ["ID","NOMBRE"], None, skip_nulls=False, null_value=-99999)#jorge
        self.lgdf = pd.DataFrame(lg)
        self.cddf = pd.DataFrame(cd)
        self.eddf = pd.DataFrame(ed)
        self.cvdf = pd.DataFrame(cv)#jorge

    # ETAPA 01
    # CONSTRUCCION DE POLIGONOS DE SIMBOLOGIA - POLIGONOS


    # CREA LA VARIABLE GRUPS PARA IDENTIFICAR SI EXISTEN COLUMNAS A LAS QUE SE LE APLICARA UN ESPACIADO | value = 1
    def getGroup(self):
        grupsTmp = list(self.lgdf[(self.lgdf[self.lg.grupo] != "-99999") | (self.lgdf[self.lg.formacion] != "-99999")][
                            self.lg.tipo].unique())
        self.grups = {1: 0, 2: 0, 3: 0}
        for x in grupsTmp:
            self.grups[x] = 1

    def nroSubcolums(self):
        subcoldf = self.lgdf.sort_values([self.lg.orden])[[self.lg.tipo, self.lg.contform]]
        self.tipos = list(self.lgdf[self.lg.tipo].unique())
        self.tipos.sort()
        controller = 0
        container = []
        current = None
        for i, r in subcoldf.iterrows():
            if r[self.lg.contform] == 1:
                if r[self.lg.tipo] == current:
                    controller = controller + 1
                else:
                    pass
            else:
                controller = 0
            container.append([controller, r[self.lg.tipo]])
            current = r[self.lg.tipo]
        self.subcol = {}
        for x in self.tipos:
            self.subcol[x] = max([m[0] for m in container if m[1] == x]) + 1

    def getCase(self):
        self.simb = simbol(self.x, self.y)
        lim = Coords(self.subcol, self.edad.xfin, self.edad.yfin).getCoord
        # pythonaddins.MessageBox(lim, "anota")

        if self.tipos in [[1, 2, 3], [1], [1, 2]]:
            C1 = ColUnidLito(self.edad.xfin, self.edad.yfin, lim[1]["xfin"])
            if lim[1]["xfin"]:
                C2 = ColMorfVolc(C1.xfin, C1.yfin, lim[2]["xfin"])
            if lim[2]["xfin"]:
                C3 = ColIntrSubv(C2.xfin, C2.yfin, lim[3]["xfin"])
            self.colums = {1: C1, 2: C2, 3: C3} if lim[2]["xfin"] else {1: C1, 2: C2}
        elif self.tipos in [[1, 3]]:
            C1 = ColUnidLito(self.edad.xfin, self.edad.yfin, lim[1]["xfin"])  # MODULE: configs | file: measure
            C3 = ColIntrSubv(C1.xfin, C1.yfin, lim[3]["xfin"])
            self.colums = {1: C1, 3: C3}
        elif self.tipos in [[2, 3]]:
            C2 = ColMorfVolc(self.edad.xfin, self.edad.yfin, lim[2]["xfin"])  # MODULE: configs | file: measure
            C3 = ColIntrSubv(C2.xfin, C2.yfin, lim[3]["xfin"])
            self.colums = {2: C2, 3: C3}

        self.colums = {k: v for k, v in self.colums.items() if k in self.tipos}

    def delRows(self, geom):
        self.outFc = {"pnt": self.GPTLeyend.path, "lin": self.GPLLeyend.path, "pol": self.GPOLeyend.path}
        with arcpy.da.UpdateCursor(self.outFc[geom], ["OID@"], self.sql) as cursorUC:
            for x in cursorUC:
                cursorUC.deleteRow()
        del cursorUC

    def loadData(self, geom, array):
        feature = {"pnt": self.jsonfiles.gpt, "lin": self.jsonfiles.gpl, "pol": self.jsonfiles.gpo}
        jsonOpen = open(feature[geom], "r")
        jsonLoad = json.load(jsonOpen)
        jsonOpen.close()
        jsonLoad["features"] = array
        json2shp = arcpy.AsShape(jsonLoad, True)
        # if geom == 'lin':
        # json2shp = arcpy.SplitLine_management(json2shp, 'in_memory\splitline')
        self.delRows(geom)
        arcpy.Append_management(json2shp, self.outFc[geom], "NO_TEST")
        return json2shp

    def cvfx(self,cvol):
        cvolc = "cvolc0" if cvol == None else cvol
        cvdf = self.cvdf.set_index("ID")
        pal = '{}'.format(unicode(cvdf.loc[cvolc]["NOMBRE"])) if len(cvolc)<=5 else cvolc
        return pal

    def anot(self, x, cur, var):
        # if '{}'.format(x.CODI) == '{}'.format(x[var]):
        if len(x[var])<5:
            return ' '.join((unicode(cur[cur.CODI == '{}'.format(x[var])][var])).split("Name")[0].split(" ")[1:])
        else:
            return x[var]

    # CREA LOS CONTENEDORES DE LOS SIMBOLOS DE LAS FORMACIONES
    # CREA LA VARIABLE simbolPolygon
    def makeForm(self):

        cursor = self.lgdf.sort_values([self.lg.orden])
        cursorpru= self.cddf.sort_values([self.lg.codi])
        ############################################################################################
        ############################################################################################
        covlcMax = cursor.groupby(self.lg.cvolc, as_index=False).agg({self.lg.orden: "max", self.lg.contform: "max"})
        covlcMax2 = covlcMax[(covlcMax.CVOLC != "-99999") | (covlcMax.CVOLC != "")].sort_values(["ORDEN"])
        ListacovlcMax3 = [x for x in covlcMax2[self.lg.cvolc]]

        serie = cursor.groupby(self.lg.serie).size()
        serie2 = cursor[cursor.CONTFORM == 1].groupby("SERIE").size()#jorge
        seriedif = serie.sub(serie2, fill_value =0)
        # serieSele = serie[serie == 1]
        serieSel = seriedif[(seriedif%1!=0)|(seriedif == 1)]
        self.ListaSerie = list(serieSel.index)#valores de cambio
        self.Listaera = [x[0:2] for x in list(serie.index)]
        self.Listasis = [x[0:3] for x in list(serie.index)]

        ############################################################################################

        self.nuevo = cursor.groupby([self.lg.serie, self.lg.serie_adi]).size()
        self.first = [i for i, x in self.nuevo.iloc[[0]].iteritems()][0]

        ############################################################################################
        ############################################################################################

        yini = self.simb.yini + self.simb.addsp #ORIGINAL SIN 250 addsp
        yini = yini +self.simb.addcr if self.first[1]!= "-999" else yini
        container = []

        controladorY = []

        tipoCurrent = None
        controller = 1
        serieuniq = False #jorge
        prevcvolc = ""
        k = 0


        ############################################################################################
        ############################################################################################

        listayini = []
        for i, x in cursor.iterrows():
            # curcvolc = x[self.lg.cvolc]
            curcvolc = self.cvfx(x[self.lg.cvolc]) if x[self.lg.cvolc] !="-99999" else x[self.lg.cvolc]

            xini = self.colums[x[self.lg.tipo]].formc["xini"]

            coords = lambda xini, yini: [[[xini, yini],
                                          [xini, yini + self.simb.heigth],
                                          [xini + self.simb.width, yini + self.simb.heigth],
                                          [xini + self.simb.width, yini],
                                          [xini, yini]]]
            ##dolor de cabeza
            # pythonaddins.MessageBox( x[self.lg.serie_adi]!="-999","mesage")
            if (x[self.lg.serie_adi]!="-999" and x[self.lg.contform] != 1) :
                yini =yini +100

                ##
            if controller != 1:
                if x[self.lg.contform] == 1:
                    if x[self.lg.tipo] == tipoCurrent:
                        k = k + 1
                        xini = xini + self.simb.contemp[x[self.lg.tipo]] * k
                    else:
                        pass
                        # yini = yini + self.simb.heigth + self.simb.separ

                        # controladorY.append(curcvolc)
                else:

                    k = 0
                    yini = yini + self.simb.heigth + self.simb.separ
                    if curcvolc in ListacovlcMax3 and x[self.lg.tipo] == tipoCurrent:

                        if curcvolc in controladorY:
                            pass

                        else:
                            # pythonaddins.MessageBox([x["ORDEN"],prevcvolc], "mesage")

                            if prevcvolc != "-99999" and prevcvolc != curcvolc:
                                yini = yini + self.simb.heigth + self.simb.separ - 300   #ORIGINAL SOLO 300
                                # controladorY.append(curcvolc)
                            else:
                                pass
                    else:

                        if (prevcvolc != "-99999" and prevcvolc!="") and prevcvolc != curcvolc :#ultima prueba no estoy seguroprevcvolc != None and prevcvolc != ""

                            yini = yini + self.simb.heigth + self.simb.separ - 300#ultima prueba no estoy seguro
                        else:
                            if (x[self.lg.serie] in self.ListaSerie and prevseradi !="-999")and x[self.lg.orden]!= 2:
                                yini = yini +250
                                # pythonaddins.MessageBox([x["ORDEN"],x["SERIE_ADI"]], "ssss")

                        # controladorY.append(curcvolc)#prueb jorge

            else:
                controller = 0
                # controladorY.append(curcvolc)#prueb jorge

            # prevcvolc = x[self.lg.cvolc]
            prevcvolc = self.cvfx(x[self.lg.cvolc]) if x[self.lg.cvolc] !="-99999" else x[self.lg.cvolc]
            #jorge condicional serieunica
            if serieuniq == False  :
                pass
            else:
                if x[self.lg.contform]==1:
                    pass
                else:

                    yini = yini+ 250#250
            ######
            tipoCurrent = x[self.lg.tipo]
            prevseradi = x[self.lg.serie_adi]
            serieuniq = x[self.lg.serie] in self.ListaSerie #jorge
            coordinates = coords(xini, yini)
            listayini.append([yini, x[self.lg.serie]])

            rows = {self.lg.codi: x[self.lg.codi],
                    self.lg.codform: None if x[self.lg.codform] == "-99999" else x[self.lg.codform],
                    self.lg.name: x[self.lg.name],
                    self.lg.grupo: None if x[self.lg.grupo] == "-99999" else self.anot( x, cursorpru, self.lg.grupo),
                    self.lg.formacion: None if x[self.lg.formacion] == "-99999" else self.anot( x, cursorpru, self.lg.formacion),
                    self.lg.deposito: None if x[self.lg.deposito] == "-99999" else x[self.lg.deposito],
                    self.lg.miembro: None if x[self.lg.miembro] == "-99999" else self.anot( x, cursorpru, self.lg.miembro),
                    self.lg.cvolc: None if x[self.lg.cvolc] == "-99999" else self.anot( x, cursorpru, self.lg.cvolc),
                    self.lg.batol: None if x[self.lg.batol] == "-99999" else x[self.lg.batol],
                    self.lg.supuni: None if x[self.lg.supuni] == "-99999" else self.anot( x, cursorpru, self.lg.supuni) ,
                    self.lg.unidad: None if x[self.lg.unidad] == "-99999" else x[self.lg.unidad],
                    self.lg.pluton: None if x[self.lg.pluton] == "-99999" else self.anot( x, cursorpru, self.lg.pluton) ,
                    self.lg.descrip: x[self.lg.descrip],
                    self.lg.serie: x[self.lg.serie],
                    self.lg.serie_adi: None if x[self.lg.serie_adi] == "-999" else x[self.lg.serie_adi],
                    self.lg.tipo: x[self.lg.tipo],
                    self.lg.contform: None if x[self.lg.contform] == -99999 else x[self.lg.contform],
                    self.lg.orden: x[self.lg.orden],
                    self.lg.hoja: x[self.lg.hoja],
                    self.lg.cuadrante: x[self.lg.cuadrante],
                    self.lg.codhoja: x[self.lg.codhoja]
                    }

            itemFeatures = {"attributes": rows, "geometry": {"rings": coordinates}}
            container.append(itemFeatures)


        self.simbolPolygon = self.loadData("pol", container)

    # ETAPA 02
    # CONSTRUCCION DE COLUMNAS Y DIVISIONES - LINEA


    # OBTIENE LA ALTURA DE LAS SIMBOLOGIAS GENERADAS
    @property
    def getHeigth(self):
        desc = arcpy.Describe(self.simbolPolygon)
        extent = json.loads(desc.extent.JSON)

        # arcpy.AddMessage(type(extent["ymax"]))
        heigth = float(extent["ymax"]) - float(extent["ymin"]) + 250.0 + 2*self.simb.addsp #ORIGINAL SOLO 250
        heigth = heigth + 2*self.simb.addcr if self.first[1]!= "-999" else heigth
        return heigth

    # CREA LAS COLUMNAS DE ACUERDO A LA OCURRENCIA
    def makeColumns(self):
        self.containerLines = []
        self.h = self.getHeigth
        for k, c in self.colums.items():
            y = c.yTop(self.h)
            coordinates = [[[c.xini, y], [c.xfin, y], [c.xfin, c.yfin], [c.xini, c.yini]]]
            itemFeatures = {
                "attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante,
                               self.lg.codhoja: self.hoja},
                "geometry": {"paths": coordinates}}
            self.containerLines.append(itemFeatures)
            head = {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante,
                                   self.lg.codhoja: self.hoja},
                    "geometry": {"paths": [[[c.xini, y - 550], [c.xfin, y - 550]]]}}
            self.containerLines.append(head)

    def divSerie(self):
        ycontainer = []
        previous = None
        self.datalg = self.lgdf.sort_values(["ORDEN"]).groupby([self.lg.serie, self.lg.serie_adi]).size()
        last = [i for i, x in self.datalg.iloc[[-1]].iteritems()][0]
        serieslist = [i for i, x in self.datalg.iteritems()]
        serieslist_in = [i for i, x in self.datalg.iteritems()]
        seriesadi = [x for x in serieslist if x[1] != '-999']



    #Toma todos los polígonos que definen los limites de serie
        for x in seriesadi:
            for p in serieslist:
                if p[0] == x[0] and p[1] == '-999':
                    # elimina formaciones intermedias que no delimitan series
                    del serieslist[serieslist.index(p)]

        for i in serieslist:
            sql = "{} = '{}' AND {}".format(self.lg.serie, i[0], self.sql)
            ytmp = max([x[0] for x in arcpy.da.SearchCursor(self.outFc["pol"], ["SHAPE@Y"], sql)])

            if i[0] in self.ListaSerie:
                y = ytmp   if i[1] != "-999" else ytmp + self.simb.elevSerie + self.simb.sercen #jorge sercen 150 final

            else:
                # define la elevacion de serie para los elementos que no tienen serieadi
                y = ytmp  if i[1] != "-999" else ytmp + self.simb.elevSerie

            ycontainer.append(y)

            if i == last and i[1] == "-999":
                del ycontainer[-1]

        elm = len(serieslist)
        for i in seriesadi:
            p = serieslist.index(i)
            cc = serieslist_in.index(i)
            if p != elm:
                if serieslist[p + 1][0] != i[1]:
                    jly = serieslist_in[cc+1][1] if serieslist_in[cc+1][1] != '-999' else None #ADD
                    sql = "{} = '{}' AND {} = '{}' AND {}".format(self.lg.serie, i[0], self.lg.serie_adi, i[1], self.sql)
                    sqlx = "{} = '{}' AND {} = '{}' AND {}".format(self.lg.serie, serieslist[p+1][0], self.lg.serie_adi, jly, self.sql)#ADD
                    sql2 = sqlx if jly else "{} = '{}' AND {} IS NULL AND {}".format(self.lg.serie, serieslist[p+1][0], self.lg.serie_adi,  self.sql)#ADD
                    ytmp = max([x[0] for x in arcpy.da.SearchCursor(self.outFc["pol"], ["SHAPE@Y"], sql)])
                    ytmp2 = min([h[0] for h in arcpy.da.SearchCursor(self.outFc["pol"], ["SHAPE@Y"], sql2)])
                    # y = ytmp + self.simb.elevSerie + 125  #jorge connected +125 temp +175
                    y2 = (ytmp2+ytmp)/2

                    # ycontainer.append(y)
                    ycontainer.append(y2)


        xini = self.edad.serie["xini"]
        xfin = self.edad.serie["xfin"]
        itemFeatures = lambda y: {
            "attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante,
                           self.lg.codhoja: self.hoja},
            "geometry": {"paths": [[[xini, y], [xfin, y]]]}}
        series = map(itemFeatures, ycontainer)
        self.containerLines.extend(series)
        self.divSisEra("eratema")
        self.divSisEra("sistema")
        self.makeColAge("eratema")
        self.makeColAge("sistema")
        self.makeColAge("serie")
        self.makeColAge("edad")
        self.simbolPolyline = self.loadData("lin", self.containerLines)



    def count(self,ed):
        x = self.Listaera if ed == "eratema" else self.Listasis
        y = []
        for i in x:
            if x.count(i) == 1:
                y.append(i)
        return y

    def divSisEra(self, edad):

        ##############################
        datalg = self.lgdf.sort_values(["ORDEN"]).groupby([self.lg.serie, self.lg.serie_adi]).size()
        serieslist = [i for i, x in datalg.iteritems()]
        seriesadi2 = [x[-1] for x in serieslist if x[1] != '-999']

        ###############################################


        ycontainer = []
        previous = None
        previous2 = 0#jorge
        previous3 = 0#jorge
        prevcvolc = ""
        ages = {"eratema": {
            "xini": self.edad.eratm["xini"],
            "xfin": self.edad.eratm["xfin"]
        },
            "sistema": {
                "xini": self.edad.sistm["xini"],
                "xfin": self.edad.sistm["xfin"]
            }
        }


        lim = 2 if edad == "eratema" else 3

        listadiv = self.count(edad)


        # pythonaddins.MessageBox(self.ListaSerie,"hihihi")
        for i in arcpy.da.SearchCursor(self.outFc["pol"], [self.lg.serie, self.lg.serie_adi, "SHAPE@Y",self.lg.orden,self.lg.contform,self.lg.cvolc], self.sql):
            if previous != None:
                if (i[0][0:lim] != previous) :


                    if i[4] ==1:#contform para cambio de sistema y eratema
                        pass
                    else:
                        y = i[2] - self.simb.elevSerie
                        #jorge conditional
                        if i[0] in self.ListaSerie and i[1] == None:
                            # pythonaddins.MessageBox([i[3],previous3 in self.ListaSerie and previous2], edad)

                            y1 = y - 250
                            y1 = y1+self.simb.sercen if previous3 in self.ListaSerie else y1 + 250 #jorge sercen 150 final
                            # if (prevcvolc != None and prevcvolc != "") and i[5] != None:#jorge luis no estoy seguro
                            #     y1 = y1 -250                        #jorgeluis no estoy seguro
                            y1 = y1+75 if  previous3 in self.ListaSerie and previous2 else y1 #parche2


                        else:
                            # y1 = y -100 if i[0] in self.ListaSerie else y
                            y1 = y -100  if i[0] in self.ListaSerie  else y
                            # y1= y1-75 if i[3]==2 else y1#parcheeeee
                            y1= y1-75 if previous3  in self.ListaSerie and ((i[1]or i[3]==2 and previous2 == None) or previous2 == None ) else y1#parcheeeee
                            # pythonaddins.MessageBox([i[3],edad,previous3  in self.ListaSerie and ((i[1]or i[3]==2 and previous2 == None) or previous2 == None ) ], "mesage serie")




                        ###########EN ANALISIS#############################22i4-22i2
                        y2 = y1- 125 if previous2 in seriesadi2 and previous3 in self.ListaSerie else y1#jorge connected-125
                        # y2 = y1
                        if (prevcvolc != None and prevcvolc != "") :  # jorge luis no estoy seguro
                            y2 = y2 - 250 if self.cvfx(i[5]) != self.cvfx(prevcvolc) else y2
                            # pythonaddins.MessageBox(i[3], "250")
                        ycontainer.append(y2)

                        if i[1] != None:

                            if (i[0][0:lim] != i[1][0:lim]) and i[1]:
                                y = i[2]
                                y2 = y

                                ycontainer.append(y2)

                elif i[1] != None:

                    if (i[0][0:lim] != i[1][0:lim]) and i[1]:
                        y = i[2]
                        y2 = y
                        ycontainer.append(y2)



            else:
                if i[1] != None:
                    if (i[0][0:lim] != i[1][0:lim]) and i[1]:
                        y = i[2]
                        y2 = y - 125 if previous2 in seriesadi2 else y  # jorge
                        ycontainer.append(y2)



            previous = i[1][0:lim] if i[1] != None else i[0][0:lim]
            #jorge

            previous2 = i[1]
            previous3 = i[0]
            prevcvolc = i[5]

        xini = ages[edad]["xini"]
        xfin = ages[edad]["xfin"]
        itemFeatures = lambda y: {
            "attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante,
                           self.lg.codhoja: self.hoja},
            "geometry": {"paths": [[[xini, y], [xfin, y]]]}}
        series = map(itemFeatures, ycontainer)
        self.containerLines.extend(series)



    def makeColAge(self, ageSelect):
        colums = {
            "eratema": self.edad.eratm,
            "sistema": self.edad.sistm,
            "serie": self.edad.serie,
            "edad": self.edad.edad
        }
        xini = colums[ageSelect]["xini"]
        xfin = colums[ageSelect]["xfin"]
        yini = colums[ageSelect]["yini"]
        yfin = self.edad.yTop(self.h)

        itemFeatures = [{"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante,
                                        self.lg.codhoja: self.hoja},
                         "geometry": {
                             "paths": [[[xini, yini], [xini, yfin], [xfin, yfin], [xfin, yini], [xini, yini]]]}}]
        self.containerLines.extend(itemFeatures)
        head = {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante,
                               self.lg.codhoja: self.hoja},
                "geometry": {"paths": [[[xini, yfin - 550], [xfin, yfin - 550]]]}}
        self.containerLines.append(head)

    def main(self):
        self.dfpandas()
        self.nroSubcolums()
        # self.getGroup()
        self.getCase()
        self.makeForm()
        self.makeColumns()
        self.divSerie()
        arcpy.RefreshActiveView()


#
# foo = Legend('29p3', "CODHOJA = '29p3'")
# foo = Legend('30q2', "CODHOJA = '30q2'")
# foo = Legend('21i4', "CODHOJA = '21i4'")
# foo.main()



