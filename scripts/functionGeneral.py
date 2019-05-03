# -*- coding: utf-8 -*-
from configs.model import *


class functionCode:
    def __init__(self, row=None, column=None, quad=None):
        self.row = row
        self.column = column.lower() if column else None
        self.quad = quad

    @property
    def makeCode(self):
        if self.quad:
            code = u'{}{}{}'.format(self.row,
                                    self.column,
                                    self.quad)
        else:
            code = u'{}-{}'.format(self.row,
                                   self.column)
        return code

    def makeQuery(self, feature=50):
        code = self.makeCode
        if feature == 50:
            query = u"{} = '{}'".format(FGeneral().codhoja,
                                        code)
        return query

    def _codeTransform(self, code, of=50, quad=None):
        if of == 50:
            res = u'{}-{}'.format(code[:-2], code[-2])
        elif of == 100:
            res = code.replace("-", '')
        return res
