# -*- coding: utf-8 -*-

from model import *
from math import ceil


class FeaturesUse:
    def __init__(self, zone):
        self.items = {
            1: {
                'fc': Pog(zone),
                "name": u'Punto de observación geológica',
                'geom': 'gpt'
            },
            2: {
                'fc': Pog(zone),
                "name": 'Dato estructural',
                'geom': 'gpt'
            },
            3: {
                'fc': Dataciones(zone),
                'name': u'Geocronología',
                'geom': 'gpt'
            },
            4: {
                'fc': Fosiles(zone),
                'name': u'Fósil',
                'geom': 'gpt'
            },
            5: {
                'fc': GptVolcanico(zone),
                'name': u'Estructura volcánica',
                'geom': 'gpt'
            },
            6: {
                'fc': GplContactoGeologico(zone),
                'name': u'Contacto Geológico',
                'geom': 'gpl'
            },
            7: {
                'fc': GplDique(zone),
                'name': u'Estructura ígnea',
                'geom': 'gpl'
            },
            8: {
                'fc': GplVolcanico(zone),
                'name': u'Estructura volcánica',
                'geom': 'gpl'
            },
            9: {
                'fc': GplGeomorfologia(zone),
                'name': 'Geoforma',
                'geom': 'gpl'
            },
            10: {
                'fc': GplSeccion(zone),
                'name': u'Sección',
                'geom': 'gpl'
            },
            11: {
                'fc': GplFallas(zone),
                'name': 'Falla',
                'geom': 'gpl'
            },
            12: {
                'fc': GplPliegues(zone),
                'name': 'Pliegue',
                'geom': 'gpl'
            },
            13: {
                'fc': "",
                'name': '',
                'geom': 'gpl'
            },
            14: {
                'fc': GpoAlteraciones(zone),
                'name': u'Zona de alteración',
                'geom': 'gpo'
            },
            15: {
                'fc': GpoMetamorfica(zone),
                'name': u'Zona metamórfica',
                'geom': 'gpo'
            },
            16: {
                'fc': GpoGeomorfologia(zone),
                'name': 'Geoforma',
                'geom': 'gpo'
            }
        }


class MeasureSymbols:
    def __init__(self):
        self.ini = {
            "x": 10000.0,
            "y": 10000.0,
        }
        self.rows = 15.0
        self.h = 250.0
        self.wcol = 3000 +250
        self.simb = {
            "w": 500.0,
            "h": 250
        }
        self.vacio = 125.0

    def get_params(self, idx):
        col = ceil(idx / self.rows)
        self.jcol=col-1
        xini = self.ini['x'] + self.wcol * (col - 1)
        idx = idx - (self.rows * (col - 1))
        return {"xini": xini, "idx": idx}

    def get_coordinates_title(self, idx):
        coord = {}
        dat = self.get_params(idx)
        y = lambda m: self.ini['y'] - self.h * m - (self.h / 2.0)
        coord["x"] = dat["xini"] + self.vacio
        coord["y"] = y(dat["idx"])
        return coord

    def get_coordinates_decription(self, idx):
        coord = {}
        dat = self.get_params(idx)
        y = lambda m: self.ini['y'] - self.h * m - (self.h / 2.0)
        coord["x"] = dat["xini"] + self.vacio * 2 + self.simb["w"]
        coord["y"] = y(dat["idx"])
        return coord

    def get_coordinates_point(self, idx):
        coord = {}
        dat = self.get_params(idx)
        y = lambda m: self.ini['y'] - self.h * m - (self.h / 2.0)
        coord["x"] = dat["xini"] + self.vacio + (self.simb['w'] / 2.0)
        coord["y"] = y(dat["idx"])
        return coord

    def get_coordinates_line(self, idx):
        coord = []
        dat = self.get_params(idx)
        y = lambda m: self.ini['y'] - self.h * m - (self.h / 2.0)
        coord.append([dat["xini"] + self.vacio, y(dat["idx"])])
        coord.append([dat["xini"] + self.vacio + self.simb['w'], y(dat["idx"])])
        return coord

    def get_coordinates_polygon(self, idx):
        coord = []
        dat = self.get_params(idx)
        y = lambda m: self.ini['y'] - self.h * m
        coord.append([dat["xini"] + self.vacio, y(dat["idx"]) - 50])
        coord.append([dat["xini"] + self.vacio + self.simb["w"], y(dat["idx"]) - 50])
        coord.append([dat["xini"] + self.vacio + self.simb["w"], y(dat["idx"]) - self.h + 50])
        coord.append([dat["xini"] + self.vacio, y(dat["idx"]) - self.h + 50])
        coord.append([dat["xini"] + self.vacio, y(dat["idx"]) - 50])
        return coord
