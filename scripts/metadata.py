# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import arcpy
import os
from configs.model import *
from configs.statics import *
from configs.config_metadatos import *

arcpy.env.overwriteOutput = True


class MakeMetadata:
    def __init__(self, pathmxd, codhoja):
        self.codhoja = codhoja
        self.pathmxd = os.path.abspath(pathmxd)
        self.translator = Translators().TR01
        self.xmltemplate = Translators().xmltempl
        self.pathxml = os.path.join(Template().outxml,
                                    "{}.xml".format(codhoja))

    def getInfo(self):
        fc = TbMetadata()
        sql = "{} = '{}'".format(fc.codhoja, self.codhoja)
        self.info = [x for x in arcpy.da.SearchCursor(fc.path, FieldUse().fields, sql)]

    def setAttr(self):
        mxd = arcpy.mapping.MapDocument(self.pathmxd)
        mxd.title = u'{}'.format(self.info[0][0])
        mxd.summary = u'{}'.format(self.info[0][1])
        mxd.description = u'{}'.format(self.info[0][2])
        mxd.author = u'{}'.format(self.info[0][3])
        mxd.credits = u'{}'.format(self.info[0][4])
        mxd.tags = u'{}'.format(self.info[0][5])
        mxd.hyperlinkBase = u'{}'.format(self.info[0][6])
        mxd.save()
        del mxd

    def exportXML(self):
        filexml = os.path.join(os.path.dirname(__file__), 'temp.xml')
        arcpy.ExportMetadata_conversion(self.pathmxd, self.translator, filexml)
        tree = ET.parse(filexml)
        native = tree.find(ElementXML().native)
        self.native = native.text

    def setXML(self):
        tree = ET.parse(self.xmltemplate)

        title = tree.find(ElementXML().title)
        title.text = u'{}'.format(self.info[0][0])

        summary = tree.find(ElementXML().summary)
        summary.text = u'{}'.format(self.info[0][1])

        description = tree.find(ElementXML().description)
        description.text = u'{}'.format(self.info[0][2])

        credits = tree.find(ElementXML().credits)
        credits.text = u'{}'.format(self.info[0][4])

        uselimit = tree.find(ElementXML().uselimit)
        uselimit.text = u'{}'.format(self.info[0][-1])

        native = tree.find(ElementXML().native)
        native.text = u'{}'.format(self.native)

        tags = tree.find(ElementXML().theme)
        for tg in (self.info[0][5]).split(","):
            child = ET.Element('themekey')
            child.text = tg
            tags.append(child)

        tree.write(self.pathxml)

    def deletingLog(self):
        direct = os.path.dirname(self.pathxml)
        for x in os.listdir(direct):
            if x.split(".")[-1] == 'log':
                os.remove(os.path.join(direct, x))

    def setMetadataMXD(self):
        arcpy.ImportMetadata_conversion(self.pathxml, "FROM_FGDC",
                                        self.pathmxd, 'ENABLED')

    def process(self):
        self.getInfo()
        if len(self.info) != 0:
            self.setAttr()
            self.exportXML()
            self.setXML()
            self.setMetadataMXD()
            self.deletingLog()
        else:
            pass

    def main(self):
        self.process()
