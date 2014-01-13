#!/usr/bin/env python

"""Using jinja2, and webapp2, this defines the main website logic
   for this application. There will be two pages: a mainpage, with
   a few pieces of information relating to order of operations in
   arithematic, problem solving strategies for polynomial equations,
   and how to use the quadratic equation. This page will be updated
   as new problem types are developed.
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

# set up the load path for jinja2 templating functionality.
# all html is located in the views directory, while css is
# found in the static directory.
td = os.path.join(os.path.dirname(__file__),'views')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(td),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    """A generic request handler, wrapping the webapp2.request...
       and implementing jinja2 string/document rendering"""
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
        
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

        
class MainPage(Handler):
    """The initial, root webpage. This holds some auxilary knowledge,
       and a button, linking to the exam page."""
    
    def get(self):
        """Initialize two sample problems, to test whether the
           user should visit a side link."""
        u = User('guest')
        self.a = Arm(u)
        self.b = Alg(u)
        self.a.build_problem()
        self.b.build_problem()
        self.render('mainpage.html',algebraic = self.b.to_html(),
                    arithematic = self.a.to_html())

    def post(self):
        #if name == 'continue':
        #    self.redirect()
        #elif name == 'algebra':
        #    if self.a.validate(ans):
        #        self.render_str("yay")
        #    else:
        #        self.render_str("boo")
        #else:
        #    if self.b.validate(ans):
        #        self.render_str("yay")
        #    else:
        #        self.render_str("boo")
        pass
    
    def redirect(self):
        pass

class QuestionPage(Handler):
    """The question page. Upon connecting to this page, a dummey user
       object will be created to store the current users score and
       times. A question will be created with the get method, and
       on subsequent post methods, relating to answering questions,
       (either prompting a new question, or re-prompting for a 
       solution)
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

