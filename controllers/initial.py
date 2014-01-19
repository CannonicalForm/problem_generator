#!/usr/bin/env python

from base import Handler
from base import env
from models import validate
from models import search_by_user
from models import next_question
from google.appengine.api import users

class InitialPage(Handler):
    def __init__(self,*args,**kwargs):
        super(InitialPage,self).__init__(*args,**kwargs)
        self.template = env.get_template('mainpage.html')

    def get(self):
        user = users.get_current_user()
        if user:
            current = search_by_user(user.user_id())
            stmt = current.sample_stmt[0]+' '+current.sample_stmt[1]
            context = self.context.extend({'stmt':stmt,
                                           'user':user,
                                           'nickname':current.user.email(),
                                           'is_valid':current.valid})
        else:
            context = self.context
        self.render(self.template,**context)

    def post(self):
        user = users.get_current_user()
        current = search_by_user(user.user_id())
        answer = self.request.get('answer')
        if validate(answer,current.sample_sol):
            current.valid = "Correct"
        else:
            current.valid = "Try Again"
        current.put()
        self.get()
            





