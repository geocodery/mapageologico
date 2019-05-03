# -*- coding: utf-8 -*-

from model import *


class ElementXML:
    def __init__(self):
        self.title = "***/title"
        self.tags = "***/themekey"
        self.summary = "**/purpose"
        self.description = "**/abstract"
        self.credits = "*/datacred"
        self.uselimit = "*/useconst"
        self.native = "*/native"
        self.theme = '**/theme'


class FieldUse():
    def __init__(self):
        self.fc = TbMetadata()
        self.fields = [
            self.fc.nombre,
            self.fc.resumen,
            self.fc.descripcion,
            self.fc.autor,
            self.fc.creditos,
            self.fc.tag,
            self.fc.enlace,
            self.fc.usos_lim
        ]
