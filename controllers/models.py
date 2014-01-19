#!/usr/bin/env python

import random
from scripts.algebraic import Algebraic
from scripts.calc import Arithematic
from google.appengine.ext import db
from google.appengine.api import users
from fractions import Fraction as f

class CurrentQuestion(db.Model):
    user = db.UserProperty(auto_current_user_add = True)
    sample_stmt = db.ListProperty(str)
    sample_sol = db.ListProperty(str)
    stmt = db.ListProperty(str)
    solution = db.ListProperty(str)
    attempts = db.IntegerProperty(default = 0)
    solved = db.IntegerProperty(default = 0)
    level = db.IntegerProperty(default = 0)
    previous = db.ListProperty(str)
    valid = db.StringProperty()
    

def search_by_user(user_id = None):
    if not user_id:
        user = users.get_current_user()
        if not user:
            return None
        user_id = user.user_id()
    key = db.Key.from_path('CurrentQuestion',user_id)
    current = db.get(key)
    if not current:
        sample_sol,sample_stmt = next_question(0)
        solution,html = next_question(0)
        current = CurrentQuestion(key_name = user_id)
        current.attempts = 0
        current.solved = 0
        current.level = 0
        current.previous = []
        current.solution = solution
        current.stmt = html
        current.valid = ''
        current.sample_stmt = sample_stmt
        current.sample_sol = sample_sol
        current.put()
    return current


def next_question(difficulty):
    if random.random() < 0.5 + difficulty*.1:
        q = Arithematic()
    else:
        q = Algebraic()
    html = q.to_html()
    return (map(str,q.solution),html)
    

def validate(answer,sol):
    solution = set()
    answers = set()
    for s,ans in zip(answer.split(),sol):
        ans = map(int,ans.split('/'))
        s = map(int,s.split('/'))
        if len(s) == 1:
            solution.add(f(s[0],1))
        else:
            solution.add(f(*s))
        if len(ans) == 1:
            answers.add(f(ans[0],1))
        else:
            answers.add(f(*ans))
    return solution == answers


