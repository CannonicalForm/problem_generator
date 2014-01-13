#!/usr/bin/env python

"""This module will hold the main lexing and parsing logic of the program."""

import re
import ply.lex as lex
import ply.yacc as yacc
from fractions import Fraction as f


tokens = ('NUMBER','LPAREN','RPAREN','PLUS','MINUS','TIMES')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_ignore = "  \t"

def t_NUMBER(t):
    r'-?[0-9]+/[0-9]+|-?[0-9]+'
    parts = re.split('/',t.value)
    if len(parts) == 1:
        parts.append(1)
    t.value = f(*map(int,parts))
    return t

def t_error(t):
    print t.value
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

lex.lex(debug = 0, optimize = 1, lextab = None)

precedence = (('left','PLUS','MINUS'),('left','TIMES'))

def p_error(p):
    print "Unexpected : '%s'" %(p)

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression'''
    if p[2]   == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

parser = yacc.yacc(debug = 0, optimize = 1,
                   write_tables = 0)

if __name__ == "__main__":
    assert parser.parse("4 + 4") == 8
    assert parser.parse("3/4 + 4/4") == f(7,4)
    assert parser.parse("2 - 3") == -1
    assert parser.parse("2 * 4") == 8
    assert parser.parse("2 + 4 * 7") == 30
    assert parser.parse("(2 + 3) * 5") == 25
    assert parser.parse("3/4 - 1/4") == f(1,2)
    assert parser.parse("0/4 * 9") == 0
