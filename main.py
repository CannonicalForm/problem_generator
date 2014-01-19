#!/usr/bin/env python

"""Using jinja2, and webapp2, this defines the main 
   website logic for this application. There will be two 
   pages: a mainpage, with a few pieces of information 
   relating to order of operations in arithematic, 
   problem solving strategies for polynomial equations,
   and how to use the quadratic equation. This page will 
   be updated as new problem types are developed.
"""
import webapp2
from controllers.frac import FractionPage
from controllers.polys import PolyPage
from controllers.ordops import OrderPage
from controllers.questions import QuestionPage
from controllers.userpage import UserPage
from controllers.initial import InitialPage


mainapp = webapp2.WSGIApplication([('/', InitialPage),
                               ('/fractions',FractionPage),
                               ('/polynomials',PolyPage),
                               ('/orderops',OrderPage)],
                              debug = True)

logged_in_app = webapp2.WSGIApplication([('/questions',QuestionPage),
                                         ('/users/\d+',UserPage)],
                                      debug = True)
