from model import *


class MeasureTables:
    def __init__(self, feature):
        self.fc = Dataciones(18) if feature == 'datacion' else Fosiles(18)
        self.col = 10 if feature == 'datacion' else 9
        self.ini = {
            "x": 10000.0,
            "y": 10000.0,
        }
        self.h = 250.0
        if feature == 'datacion':
            self.head = {
                1: {
                    'w': 600.0,
                    'name': self.fc.edad_ma,
                },
                2: {
                    'w': 600.0,
                    'name': self.fc.error_ma,
                },
                3: {
                    'w': 600.0,
                    'name': self.fc.utm_e,
                },
                4: {
                    'w': 600.0,
                    'name': self.fc.utm_n,
                },
                5: {
                    'w': 600.0,
                    'name': self.fc.zona,
                },
                6: {
                    'w': 600.0,
                    'name': self.fc.metodo,
                },
                7: {
                    'w': 1500.0,
                    'name': self.fc.roca,
                },
                8: {
                    'w': 2250.0,
                    'name': self.fc.unidad,
                },
                9: {
                    'w': 900.0,
                    'name': self.fc.muestra,
                },
                10: {
                    'w': 1750.0,
                    'name': self.fc.referencia,
                }
            }
        else:
            self.head = {
                1: {
                    'w': 500.0,
                    'name': self.fc.codi_muestra,
                },
                2: {
                    'w': 750.0,
                    'name': self.fc.utm_e,
                },
                3: {
                    'w': 750.0,
                    'name': self.fc.utm_n,
                },
                4: {
                    'w': 1000.0,
                    'name': self.fc.grupo_taxonomico,
                },
                5: {
                    'w': 2500.0,
                    'name': self.fc.especie,
                },
                6: {
                    'w': 1500.0,
                    'name': self.fc.edad,
                },
                7: {
                    'w': 900.0,
                    'name': self.fc.unidad,
                },
                8: {
                    'w': 1200.0,
                    'name': self.fc.cronoestratigrafia,
                },
                9: {
                    'w': 1150.0,
                    'name': self.fc.referencia,
                }
            }

    def get_initial_coordinate_cell(self, head, row):
        coord = {}
        dis = sum([v['w'] for k, v in self.head.items() if k < head])
        coord['x'] = self.ini['x'] + dis
        coord['y'] = self.ini['y'] - self.h * row
        return coord

    def get_center_coordinate_cell(self, head, row):
        coord = {}
        ini = self.get_initial_coordinate_cell(head, row)
        inix, iniy = ini['x'], ini['y']
        coord['x'] = inix + (self.head[head]['w'] / 2.0)
        coord['y'] = iniy - (self.h / 2.0)
        return coord

    def get_cell_coordinates(self, head, row):
        coords = []
        ini = self.get_initial_coordinate_cell(head, row)
        coords.append([ini['x'], ini['y']])
        coords.append([ini['x'], ini['y'] - self.h])
        coords.append([ini['x'] + self.head[head]['w'], ini['y'] - self.h])
        coords.append([ini['x'] + self.head[head]['w'], ini['y']])
        coords.append([ini['x'], ini['y']])
        return coords
