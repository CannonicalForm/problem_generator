#!/usr/bin/env python

"""This will hold the problem generation logic for algebraic 
   equations. An algebraic equation is one of the form x^2 - 4x + 4,    solve for x."""


import math
import random
from template import Problem
from fractions import gcd
from fractions import Fraction as f

class Algebraic(Problem):
    """Houses method's for constructing linear, quadratic, and 
       cubic polynomials. The polynomial is constructed first by
       choosing the number of roots, at random (see get_solution)
       and then choosing the specific roots probabalistically. 
       The actual polynomial expression is then constructed from
       the roots, and presented as a string, eg x^2 - 3x + 4.
       Since roots are specified in a Fraction data type, 
       validation assumes a space deliminated string, and
       conversion takes place within the validate method."""
    def __init__(self):
        super(Algebraic,self).__init__()
        self.solution = self.get_solution()
        self.problem = self.build_problem()
    def get_solution(self,p = .75):
        """Build the solution set. p represents the probability of
           a random root being an integer.  Currently the 
           probability breakdown of a Linear (L), Quadratic (Q) 
           and Cubic (C) equation is given by 
               -L : 20%
               -Q : 70%
               -C : 10%
        """
        x = random.random()
        if x < .2:
            num_roots = 1
        elif .2 < x < .9:
            num_roots = 2
        else:
            num_roots = 3
        roots = set()
        for _ in range(num_roots):
            if random.random() < p:
                den = 1
            else:
                den = random.randint(1,self.number_range[1])
            roots.add(f(random.randint(*self.number_range),den))
        return roots

    def build_problem(self):
        """If necessary calls get_solutions() to build the solution
           set, and proceeds to map that solution set to a string,
           representing the polynomial equation which reduces to
           that solutions set. Note that while roots to the 
           polynomial may be given as fractions, the equations will
           always be presented as an integer one."""
        common = lcm(*[a.denominator for a in self.solution])
        #Rewrite that monstrosiy below
        coeffs = map(lambda x : x[1],
                     map(lambda x : ((x[0],'') if x[1] == 1 and
                                x[0] != len(self.solution) else x),
                         enumerate(map(lambda x : x*common,
                                       make_expression(self.solution)
                                   ))))
        n = len(coeffs)
        p = ''
        for i,a in enumerate(coeffs): #I really need to rewrite this
            if a == 0:
                continue
            elif a > 0:
                if i == 0:
                    p += '%sx^%d'%(str(a),n - 1)
                elif i == n - 1:
                    p += ' + %s' %(str(a))
                elif i == n - 2:
                    p += ' + %sx' %(str(a))
                else:
                    p += ' + %sx^%d'%(str(a),n - i - 1)
            else:
                if i == 0:
                    p += '%sx^%d'%(str(a),n - 1)
                elif i == n - 1:
                    if a == 0:
                        pass
                    else:
                        p += ' - %s' %(str(-1*a))
                elif i == n - 2:
                    p += ' - %sx' %(str(-1*a))
                else:
                    p += ' - %sx^%d'%(str(-1*a),n - i - 1)
        return p

    def to_html(self):
        """Since all polynomials are given with integer 
           coefficients, it is not necessary to factor them in
        """
        return ['Solve for x in', '\('+self.problem+'\)']

    def __str__(self):
        return self.problem

def lcm(*args):
    """Compute the lcm of two or more integers"""
    def helper(a,b):
        """Computes the lcm of two arguments at a time"""
        return abs(a*b)/gcd(a,b)
    return reduce(helper,args)

def make_expression(roots):
    """Map the roots of a polynomial to the coefficients in 
       the equation defining it."""
    if len(roots) == 1:
        b = roots.copy()
        x = b.pop()
        return [1,-1*x]
    elif len(roots) == 2:
        a,b = roots
        return [1,-a - b,a*b]
    else:
        a,b,c = roots
        return [1,-(a + b + c),(c*a + c*b + a*b),-a*b*c]


if __name__ == "__main__":
    a = Algebraic()
    a.build_problem()
    assert a.validate(a.solution) == True
    print a.problem
    print a.validate(raw_input("> "))
