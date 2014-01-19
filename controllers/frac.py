#!/usr/bin/env python

from base import Handler
from base import env


class FractionPage(Handler):
    def get(self):
        template = env.get_template('fraction_tut.html')
        self.render(template)
    def post(self):
        pass






