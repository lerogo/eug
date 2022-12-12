#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .token import *
from .enum import *


class Lexer:

    def __init__(self, path):
        
        self.State = Enum.enum(
            "START",
            "EQORASSIGN",  
            "LTORLE",  
            "GTORGE",
            "INUNEQ",
            "INCOMMENT",
            "INNUM",
            "INPLUS",
            "INMINUS",
            "INID",
            "INASSIGN",
            "QUOTEORSTR",  
            "DOTORNUM",  
            "STRING",
            "ORORLOGIC",
            "ANDORLOGIC",
            "INDOT",
            "DONE")

        
        
        self.TokenType = Token.getTokenTypeList()
        self.ReservedWord = Token.getReservedWord()
        self.path = path  
        self.pos = 0  
        self.lineno = 0  
        self.curline = ""  
        self.currenToken = -1  
        self.curstate = -1  
        self.tokenString = ""
        self.__loadSource(self.path)

    def __loadSource(self, filename):
        self.source = open(filename, 'r')

    def __getNextChar(self):
        if self.pos >= len(self.curline):
            self.curline = self.source.readline()
            self.lineno += 1
            if not self.curline:
                return ""
            self.pos = 0
            self.pos += 1
            return self.curline[self.pos - 1]
        else:
            self.pos += 1
            return self.curline[self.pos - 1]

    def __ungetNextChar(self):
        self.pos -= 1

    def __lookbackChar(self):
        return self.curline[self.pos - 2]

    def __getTokenType(self, c):
        token = {
            
            
            
            "@": self.TokenType.AT,
            '{': self.TokenType.LBRACE,
            '}': self.TokenType.RBRACE,
            ',': self.TokenType.COMMA,
            '+': self.TokenType.PLUS,
            '-': self.TokenType.MINUS,
            '*': self.TokenType.TIMES,
            '/': self.TokenType.DIV,
            '(': self.TokenType.LPAREN,
            ')': self.TokenType.RPAREN,
            ';': self.TokenType.SEMI,
            '[': self.TokenType.LBRACKET,
            ']': self.TokenType.RBRACKET,
            '^': self.TokenType.POW,
            ':': self.TokenType.COL
        }
        if c in list(token.keys()):
            return token[c]
        else:
            return self.TokenType.ERROR

    def __state_START(self, c):
        self.save = True
        if c.isdigit():
            self.curstate = self.State.INNUM
        elif c.isalpha():
            self.curstate = self.State.INID
        
        
        elif c == ' ' or c == '\t' or c == '\n' or c == '\r':
            self.save = False
        elif c == "%":
            self.save = False
            self.curstate = self.State.INCOMMENT
        elif c == "~":
            self.save = True
            self.curstate = self.State.INUNEQ
        elif c == "=":
            self.save = True
            self.curstate = self.State.EQORASSIGN
        elif c == "<":
            self.save = True
            self.curstate = self.State.LTORLE
        elif c == ">":
            self.save = True
            self.curstate = self.State.GTORGE
        
        
        
        elif c == "'":
            self.save = True
            self.curstate = self.State.QUOTEORSTR
        elif c == "+":
            self.save = True
            self.curstate = self.State.INPLUS
        elif c == "-":
            self.save = True
            self.curstate = self.State.INMINUS
        elif c == "&":
            self.save = True
            self.curstate = self.State.ANDORLOGIC
        elif c == "|":
            self.save = True
            self.curstate = self.State.ORORLOGIC
        elif c == ".":
            self.save = True
            self.curstate = self.State.INDOT
        else:
            self.curstate = self.State.DONE
            self.currentToken = self.__getTokenType(c)

    def __state_EQORASSIGN(self, c):
        if c == '=':
            self.currentToken = self.TokenType.EQ
        else:
            self.curstate = self.State.INASSIGN
            self.currentToken = self.TokenType.ASSIGN
            self.__ungetNextChar();
        self.curstate = self.State.DONE

    def __state_LTORLE(self, c):
        if c == '=':
            self.currentToken = self.TokenType.LE
        else:
            self.__ungetNextChar()
            self.currentToken = self.TokenType.LT
        self.curstate = self.State.DONE

    def __state_GTORGE(self, c):
        if c == '=':
            self.currentToken = self.TokenType.GE
        else:
            self.__ungetNextChar()
            self.currentToken = self.TokenType.GT
        self.curstate = self.State.DONE

    def __state_INUNEQ(self, c):
        if c == '=':
            self.currentToken = self.TokenType.UNEQ
            self.save = True
        else:
            self.__ungetNextChar()
            self.currentToken = self.TokenType.LOGICNOT
            self.save = False
        self.curstate = self.State.DONE

    def __state_INCOMMENT(self, c):
        self.save = False
        if c == '\r' or c == '\n':
            self.curstate = self.State.START

    def __state_INNUM(self, c):
        if not c.isdigit() and c != '.' and c != 'e' and c != '-':
            self.__ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.NUM

    def __state_INID(self, c):
        if (not c.isalpha()) and (not c.isdigit()) and (c != '_'):
            self.__ungetNextChar()
            self.save = False
            self.currentToken = self.TokenType.ID
            self.curstate = self.State.DONE

    def __state_INPLUS(self, c):
        i = 3;
        LastNonEmptyChar = self.curline[self.pos - i]  

        while LastNonEmptyChar == ' ':
            i += 1
            LastNonEmptyChar = self.curline[self.pos - i]
        if not c.isdigit() or LastNonEmptyChar.isalpha() or LastNonEmptyChar.isdigit() or (LastNonEmptyChar == "_"):
            self.__ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.PLUS
        else:
            self.save = True
            self.curstate = self.State.INNUM

    
    def __state_INMINUS(self, c):
        i = 3;
        LastNonEmptyChar = self.curline[self.pos - i]  

        while LastNonEmptyChar == ' ':
            i += 1
            LastNonEmptyChar = self.curline[self.pos - i]

        if not c.isdigit() or LastNonEmptyChar.isalpha() or LastNonEmptyChar.isdigit() or (LastNonEmptyChar == "_"):
            self.__ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.MINUS
        else:
            self.save = True
            self.curstate = self.State.INNUM

    
    def __state_ANDORLOGIC(self, c):
        if c == "&":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.AND
            self.save = True
        else:
            self.__ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.LOGICAND

    
    def __state_ORORLOGIC(self, c):
        if c == "|":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.OR
            self.save = True
        else:
            self.__ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.LOGICOR

    def __state_INDOT(self, c):
        if c == "*":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.DOTTIMES
            self.save = True
        elif c == "/":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.DOTRDIV
            self.save = True
        elif c == "\\":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.DOTLDIV
            self.save = True
        elif c == "^":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.DOTPOW
            self.save = True
        elif c == "'":
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.DOTTRANSPOSE
            self.save = True
        else:
            self.__ungetNextChar()
            self.currentToken = self.TokenType.DOT
            self.curstate = self.State.DONE
            self.save = False

    
    
    
    
    
    
    
    
    

    def __state_QUOTEORSTR(self, c):
        self.__ungetNextChar()
        lookback = self.__lookbackChar()
        if lookback.isalpha() or lookback == ')':
            self.currentToken = self.TokenType.TRANSPOSE
            self.save = False
            self.curstate = self.State.DONE
        else:
            self.save = False
            self.curstate = self.State.STRING

    def __state_STRING(self, c):
        if c == "'":
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.STRING
        else:
            self.save = True

    def getToken(self):
        self.tokenStringIndex = 0
        self.tokenString = ''
        self.curstate = self.State.START

        while (self.curstate != self.State.DONE):
            c = self.__getNextChar()
            if not c:
                self.curstate = self.State.DONE
                self.save = False
                self.currentToken = self.TokenType.ENDFILE
                self.tokenString = ""
                break
            self.save = True

            {
                self.State.START: lambda x: self.__state_START(x),
                self.State.INCOMMENT: lambda x: self.__state_INCOMMENT(x),
                self.State.EQORASSIGN: lambda x: self.__state_EQORASSIGN(x),
                self.State.LTORLE: lambda x: self.__state_LTORLE(x),
                self.State.GTORGE: lambda x: self.__state_GTORGE(x),
                self.State.INUNEQ: lambda x: self.__state_INUNEQ(x),
                self.State.INNUM: lambda x: self.__state_INNUM(x),
                self.State.INID: lambda x: self.__state_INID(x),
                self.State.QUOTEORSTR: lambda x: self.__state_QUOTEORSTR(x),
                self.State.STRING: lambda x: self.__state_STRING(x),
                self.State.INPLUS: lambda x: self.__state_INPLUS(x),
                self.State.INMINUS: lambda x: self.__state_INMINUS(x),
                self.State.ANDORLOGIC: lambda x: self.__state_ANDORLOGIC(x),
                self.State.ORORLOGIC: lambda x: self.__state_ORORLOGIC(x),
                self.State.INDOT: lambda x: self.__state_INDOT(x)
                
            }[self.curstate](c)
            if self.save and c != " ":
                self.tokenString += c

        if self.curstate == self.State.DONE:
            
            if self.tokenString in list(self.ReservedWord.keys()):
                self.currentToken = self.ReservedWord[self.tokenString]

            return Token(self.tokenString, self.currentToken, self.lineno)
