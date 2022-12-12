#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .enum import *


class Token:
    def __init__(self, Value, Type, lineno=0):
        self.tokenValue = Value
        self.tokenType = Type
        self.lineno = lineno

    @staticmethod
    def getTokenTypeList():
        TypeList = Enum.enum(
            "DEF",
            "IF",
            "ELSE",
            "ELIF",
            "WHILE",
            "ID",
            "RETURN",
            "BREAK",
            "CONTINUE",
            "REQUEST",
            "EVALJS",
            "EXFILE",
            "READFILE",
            "SAVEFILE",
            "PLOT",
            "MPRO")
        return TypeList

    @staticmethod
    def getReservedWord():
        TokenType = Token.getTokenTypeList()
        ReservedWord = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'elif': TokenType.ELSEIF,
            'def': TokenType.FUNCTION,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'request': TokenType.REQUEST,
            'evaljs': TokenType.EVALJS,
            'exfile': TokenType.EXFILE,
            'readfile': TokenType.READFILE,
            'savefile': TokenType.SAVEFILE,
            'plot': TokenType.PLOT,
            'mpro': TokenType.MPRO,
        }
        return ReservedWord

    def setToken(self, Value, Type, lineno):
        self.tokenValue = Value
        self.tokenType = Type
        self.lineno = lineno
        return self
