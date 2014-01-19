#!/usr/bin/env python

from base import Handler
from base import env
from models import CurrentQuestion
from models import next_question


class UserPage(Handler):
    def get(self):
        template = env.get_template('userpage.html')
        self.render(template)
    def post(self):
        pass

