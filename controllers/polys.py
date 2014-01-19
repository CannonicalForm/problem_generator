#!/usr/bin/env python

from base import Handler
from base import env


class PolyPage(Handler):
    def get(self):
        template = env.get_template('poly_tut.html')
        self.render(template)
    def post(self):
        pass






