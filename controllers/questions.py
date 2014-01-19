#!/usr/bin/env python

"""Implement the handler for the questions page. Note that since we are
   enforcing a required login in the app.yaml file for this page,
   it is unecessary to validate a user being logged in."""

from base import Handler
from base import env
from models import CurrentQuestion
from models import next_question
from models import validate
from models import search_by_user
from google.appengine.api import users

class QuestionPage(Handler):
    def __init__(self,*args,**kwargs):
        super(QuestionPage,self).__init__(*args,**kwargs)
        self.template = env.get_template('questions.html')

    def get(self):
        """As apposed to previous impleminations, get() will be the only
           rendering method in this handler. Note that necessitates
           pulling updated CurrentQuestion information for each response,
           since the put() method most likely will change the object."""
        user = users.get_current_user()
        current = search_by_user(user.user_id())
        stmt = current.stmt[0]+' '+current.stmt[1]
        context = self.context.extend({'user':user,
                                       'nickname':user.email(),
                                       'stmt':stmt,
                                       'attempt':"",
                                       'problems':current.previous,
                                       'is_valid':current.valid,
                                       'level':current.level,
                                       'solved':current.solved,
                                       'attempts':current.attempts})
        self.render(self.template,**context)

    def post(self):
        """Validate the user input, and either prompt the user for a
           new answer, or prepare the page for a new question, by
           properly updating the CurrentQuestion entity for the
           given user."""
        user = users.get_current_user()
        current = search_by_user(user.user_id())
        answer = self.request.get('answer')
        if validate(answer,current.solution):
            current.valid = "Correct"
            current.solved += 1
            if current.solved // 10 >= current.level:
                current.level += 1
            previous = current.stmt[0]+' '+current.stmt[1]+' is solved by '
            previous += ' '.join(current.solution)
            current.previous.append(previous)
            solution,stmt = next_question(current.level)
            current.stmt = stmt
            current.solution = solution
        else:
            current.valid = "Try Again"
        current.attempts += 1    
        current.put()
        #self.redirect('/questions')
        self.get()
    







