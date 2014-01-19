#!/usr/bin/env python

"""
   The main entry point for the app. All url's are mapped to their
   respective handlers. No other logic is allowed here. Note that as
   their names would indicate, mainapp controlles the majority of sites,
   i.e. those not requiring being logged in, while logged_in_app controls
   all pages that app.yaml designates as login:required.
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
