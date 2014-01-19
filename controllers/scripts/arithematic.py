#!/usr/bin/env python


"""This will hold the problem generation logic for arithematic
   expressions"""

import random
import re
from  my_parse import parser
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
    def __init__(self):
        super(Arithematic,self).__init__()
        self.grouping = .25
        self.max_level = 1
        self.problem = self.build_problem()
        self.solution = self.get_solution()

    def build_problem(self):
        exp = Expression(self.number_range[1],
                         self.max_level,self.grouping)
        return exp.__str__()

    def get_solution(self):
        """Uses a parser build out of the ply module, instead of
           exec, which allows me to return as fractions, instead
           of performing integer division"""
        return set([parser.parse(self.problem)])

    def to_html(self):
        """Render the problem in a form that is convertable to
           TeX by MathJax. Note that inline MathJax equations are 
           bracketed by \(...\). Prepends a prompt"""
        prompt = "Reduce"
        fractions = re.findall('\d+/\d+',self.problem)
        h = '\('+self.problem+'\)'
        for f in fractions:
            a,b = f.split('/')
            text = r'\\frac{%s}{%s}'%(a,b)
            h = re.sub('\d+/\d+',text,h,count = 1)
        return [prompt,h]

        
    def __str__(self):
        return self.problem

            
if __name__ == "__main__":
    assert parser.parse("32 + 4") == 36
    a = Arithematic()
    s = a.solution.pop()
    print str(a)+' = '+str(s)
    assert parser.parse(str(a)) == s
    print a,
    print a.to_html()[1]
    print a.new_to_html()
    #ans = raw_input("> ")
    #print a.validate(ans)
