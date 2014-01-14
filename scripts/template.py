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
    def __init__(self,user):
        self.user = user
        self.difficulty = user.level
        self.number_range = (0,12)
    def build_problem(self):
        pass
    def get_solution(self):
        pass
    def validate(self,ans):
        pass

class Test_User:
    """A simple user class, which holds the ratio of correct 
       answers to attempts, and the average time taken to
       complete each problem."""
    def __init__(self,name,level = 0):
        self.level = level
        self.name = name
        self.correct = 0
        self.attempts = 0
    def __str__(self):
        return "User: %s, with level %s"%(self.name,self.level)

    def raise_level(self):
        pass


if __name__ == "__main__":
    u = Test_User('casey')
    p = Problem(u)
    print dir(p)

