# -*- coding: utf-8 -*-

class Error(Exception):
    pass


class ParseError(Error):

    def __init__(self, message, expression=None):
        self.expression = expression
        self.message = message


class ParamError(Error):

    def __init__(self, message, expression=None):
        self.message = message
        self.expression = expression
