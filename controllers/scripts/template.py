#!/usr/bin/env python


"""This is going to hold a problem base class."""

class Problem(object):
    """"The base class for all problems. The governing call method
        is to pass a user into the problem, the user should have
        a ration_correct attribute. Then, perform the following
        sequence of steps:
            u = User(*args,**kwargs)
            p = Problem(u)
            p.build_problem()
            #Display the problem in some method
            #Prompt the user for a solution, and store that solution
            #as a or someting
            p.validate(a)
            if True:
               call another problem,
            else:
               re-display the problem, and prompt the user for 
               another solution.
    """
    def __init__(self,difficulty = 0):
        self.difficulty = difficulty
        self.number_range = (0,12)
    def build_problem(self):
        pass
    def get_solution(self):
        pass




