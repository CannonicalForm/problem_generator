#!/usr/bin/env python

from base import Handler
from base import env


class OrderPage(Handler):
    def get(self):
        template = env.get_template('order_tut.html')
        self.render(template)
    def post(self):
        pass






