#!/usr/bin/env python

"""A simple testing suite for manually testing the problem
   generating modules, in a command line environment. There
   are three optional aguments when running this program:
      -h      : show useage
      -p x    : set probability to x
      -n y    : run the progam n times
      -u name : set the users name to name
"""

import argparse
from random import random
from calc import Arithematic as Arm
from calc import arm_validate as arm_v
from algebraic import Algebraic as Alg
from algebraic import alg_validate as alg_v
from template import Test_User
from sys import argv
from time import time

def present_problem(user,p = .5):
    """Choose and present either an arithematic or
     algebraic problem, based on the probability p.
     Prompt the user for a solution, and validate
     that solution."""
    if random() < p:
        problem = Arm(user)
    else:
        problem = Alg(user)
    problem.build_problem()
    print problem.problem
    t1 = time()
    answer = raw_input("Enter a solution: ")
    while problem.validate(answer) is False:
        answer = raw_input("Incorrect- Enter a solution: ")
    t2 = time()
    dt = t2 - t1
    print "Correct: %d, Attempts: %d, Time: %.2f" %(user.correct,
                                                  user.attempts,
                                                  dt)
    return

def main():
    parser = argparse.ArgumentParser(add_help = True)
    parser.add_argument('-n',action = 'store',dest = 'n',
                        default = '10',type =int,
                        help = "Number of times to run test")
    parser.add_argument('-u',action = 'store',dest = 'name',
                        default = 'Casey',
                        help = "User name to pass to the program")
    parser.add_argument('-p',action = 'store',dest ='p',
                        default = .5,type=float,
                        help = '''Probability of getting an 
                        arithematic problem''')
    results = parser.parse_args()
    u = Test_User(results.name)
    for i in range(results.n):
        present_problem(u,results.p)

if __name__ =="__main__":
    main()
