from model import *


class FieldsUse:
    def __init__(self):
        self.tb = tblegend()
        self.fields = [
            self.tb.codi,
            self.tb.name,
            self.tb.hoja,
            self.tb.cuadrante,
            self.tb.codhoja
        ]
