#!/usr/bin/env python


"""This will hold the problem generation logic for arithematic
   expressions"""

import math
import random
import re
from  my_parse import parser
from template import Test_User
from template import Problem
from fractions import Fraction as f

class Expression:
    OPS = ['+','-','*']

    def __init__(self,max_numb,max_depth,grouping,depth = 0):
        """Recursively build an arithematic equation, using only
           the operations given in OPS. Note that the expression is
           given by fractional numbers, and expects a fractional 
           response. However, currently there is an 80% chance 
           of any given fractional number being an integer."""
        if (depth < max_depth and
            random.randint(0,max_depth) > depth):
            self.left = Expression(max_numb,max_depth,
                                   grouping,depth + 1)
        else:
            p = random.random()
            if p < .4:
                den = 1
            else:
                den = random.randint(1,max_numb)
            self.left = f(random.randint(1,max_numb),den)
        if (depth < max_depth
            and random.randint(0,max_depth) > depth):
            self.right = Expression(max_numb,
                                    max_depth,grouping,depth + 1)
        else:
            p = random.random()
            if p < .8:
                d = 1
            else:
                d = random.randint(1,max_numb)
            self.right = f(random.randint(1,max_numb),d)
        self.grouped = random.random() < grouping
        self.operator = random.choice(Expression.OPS)


    def __str__(self):
        s = '{0!s} {1} {2!s}'.format(self.left,self.operator,
                                     self.right)
        if self.grouped:
            return '({0})'.format(s)
        else:
            return s

    
class Arithematic(Problem):
    """Hold all necessary methods for evaluating an arithematic
       expression, inheriting from Problem."""
    def __init__(self,user):
        Problem.__init__(self,user)
        self.grouping = .25
        self.max_level = 1

    def build_problem(self):
        exp = Expression(self.number_range[1],
                         self.max_level,self.grouping)
        self.problem = exp.__str__()
        self.get_solution()

    def get_solution(self):
        """Uses a parser build out of the ply module, instead of
           exec, which allows me to return as fractions, instead
           of performing integer division"""
        self.solution = parser.parse(self.problem)

    def to_html(self):
        """Render the problem in a form that is convertable to
           TeX by MathJax. Note that inline MathJax equations are 
           bracketed by \(...\). Prepends a prompt"""
        prompt = "Reduce"
        fractions = re.findall('\d+/\d+',self.problem)
        texed = []
        h = '\('+self.problem+'\)'
        for f in fractions:
            a,b = f.split('/')
            text = r'\\frac{%s}{%s}'%(a,b)
            h = re.sub('\d+/\d+',text,h)
        return prompt + h
    
    def validate(self,answer):
        """Given a solution as a string, such as 4/3, map that 
           string into a fraction data type, and perform answer
           validation."""
        a = map(int,answer.split('/'))
        if len(a) == 1:
            ans = f(a[0],1)
        else:
            ans = f(*a)
        if self.solution == ans:
            self.user.correct += 1
            self.user.attempts += 1
            return True
        else:
            self.user.attempts += 1
            return False
        
    def __str__(self):
        return self.problem




            
if __name__ == "__main__":
    assert parser.parse("32 + 4") == 36
    u = Test_User('casey',0)
    a = Arithematic(u)
    a.build_problem()
    print a,
    print '= '+str(a.solution)
    print a.to_html()
    #ans = raw_input("> ")
    #print a.validate(ans)