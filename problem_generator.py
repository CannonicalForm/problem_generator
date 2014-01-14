#!/usr/bin/env python

"""Using jinja2, and webapp2, this defines the main 
   website logic for this application. There will be two 
   pages: a mainpage, with a few pieces of information 
   relating to order of operations in arithematic, 
   problem solving strategies for polynomial equations,
   and how to use the quadratic equation. This page will 
   be updated as new problem types are developed.
"""

import re
import webapp2
import urllib
import jinja2
import os
import random
import time
from  scripts.calc import Arithematic as Arm
from scripts.algebraic import Algebraic as Alg
from scripts.template import Test_User as User

# set up the load path for jinja2 templating functionality
# all html is located in the views directory, while css is
# found in the static directory.
td = os.path.join(os.path.dirname(__file__),'views')
env = jinja2.Environment(loader = 
                         jinja2.FileSystemLoader(td),
                         autoescape = True)

#Dirty, dirty hack
alg_problems = []
arm_problems = []


class Handler(webapp2.RequestHandler):
    """A generic request handler, wrapping the 
       webapp2.request and implementing jinja2 
       string/document rendering"""
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
        
    def render_str(self,template,**params):
        t = env.get_template(template)
        return t.render(params)
        
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))


class MainPage(Handler):
    """The initial, root webpage. This holds some 
       introductory information, as well as two sample
       problems, and a link to the exam page."""

    def __init__(self,*args,**kwargs):
        self.initialize(*args,**kwargs)
        self.u = User("guest")
        alg = Alg(self.u)
        arm = Arm(self.u)
        global alg_problems #basically this ridiculousness about the
        global arm_problems #global lists is to prevent MainPage from
        alg_problems.append(alg) #forcing a new problem on us every
        arm_problems.append(arm) #time we attempt a solution through
        alg_problems = [alg_problems[0]] #the post method. It's ugly as
        arm_problems = [arm_problems[0]] #hell, but it works
        self.alg = alg_problems[0]
        self.arm = arm_problems[0]
        self.alg_prompt,self.alg_stmt = self.alg.to_html()
        self.arm_prompt,self.arm_stmt = self.arm.to_html()
    

    def get(self):
        self.render('mainpage.html',
                    arm_prompt = self.arm_prompt,
                    arm_question = self.arm_stmt,
                    alg_prompt = self.alg_prompt,
                    alg_question = self.alg_stmt,
                    arm = "",
                    alg = "",
                    correct_or_not1 = "",
                    correct_or_not2 = "")

    def post(self):
        arm_answer = self.request.get('arm_answer') 
        alg_answer = self.request.get('alg_answer') 
        v1,v2 = "",""
        if arm_answer:
            v1 = self.arm.validate(arm_answer)
        if alg_answer:
            v2 = self.alg.validate(alg_answer)
        if arm_answer is None:
            arm_answer = ""
        if alg_answer is None:
            alg_answer = ""
        self.render('mainpage.html',
                    arm_prompt = self.arm_prompt,
                    arm_question = self.arm_stmt,
                    alg_prompt = self.alg_prompt,
                    alg_question = self.alg_stmt,
                    arm = arm_answer,
                    alg = alg_answer,
                    correct_or_not1 = v1,
                    correct_or_not2 = v2)

    def redirect(self):
        pass

class QuestionPage(Handler):
    """The question page. Upon connecting to this page, 
       a dummey user object will be created to store the 
       current users score and times. A question will be 
       created with the get method, and on subsequent 
       post methods, relating to answering questions,
       (either prompting a new question, or re-prompting 
       for a solution)
    """
    def get(self):
        pass
        
    def post(self):
        pass

class FractionPage(Handler):
    def get(self):
        self.render('fraction_tut.html')

    def post(self):
        pass

class PolyPage(Handler):
    def get(self):
        self.render('poly_tut.html')
    def post(self):
        pass

class OrderPage(Handler):
    def get(self):
        self.render('order_tut.html')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/question\d+',QuestionPage),
                               ('/fractions',FractionPage),
                               ('/polynomials',PolyPage),
                               ('/orderops',OrderPage)],
                              debug = True)

