#!/usr/bin/env python

"""
   Holds all data related objects and functions. Includes the primary data
   type, CurrentUser, which is indexed by the current user, as well as
   a custom search_or_create function, using the user_id as a key.
   Validate is also here, making this the sole entry point for interacting
   with problem types.
"""

import random
from scripts.algebraic import Algebraic
from scripts.arithematic import Arithematic
from google.appengine.ext import ndb
from google.appengine.api import users
from fractions import Fraction as f

class CurrentQuestion(ndb.Model):
    user = ndb.UserProperty(auto_current_user_add = True)
    sample_stmt = ndb.StringProperty(repeat = True)
    sample_sol = ndb.StringProperty(repeat = True)
    stmt = ndb.StringProperty(repeat = True)
    solution = ndb.StringProperty(repeat = True)
    attempts = ndb.IntegerProperty(default = 0)
    solved = ndb.IntegerProperty(default = 0)
    level = ndb.IntegerProperty(default = 0)
    previous = ndb.StringProperty(repeat = True)
    valid = ndb.StringProperty()
    

def search_by_user(user_id = None):
    """Searches the datastore by user_id, and if no entity is found,
       creates one, and instantiates it with all necessary attributes."""
    if not user_id:
        user = users.get_current_user()
        if not user:
            return None
        user_id = user.user_id()
    key = ndb.Key('CurrentQuestion',user_id)
    current = key.get()
    if not current:
        sample_sol,sample_stmt = next_question(0)
        solution,html = next_question(0)
        current = CurrentQuestion(id = user_id)
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
    """Return a new question to overwrite the stmt, solution attributes on
       the CurrentQuestion entity. As the difficulty increases more
       algebraic questions will be created than arithematic. Further,
       increased difficulty will result in more challenging problem types,
       using an increasing proportion of fractions, and an expanding
       range of solutions. The base starts with a solution range of
       (0,12), and a proportion of fractions of 20%."""
    if random.random() < 0.5 + difficulty*.1:
        q = Arithematic()
    else:
        q = Algebraic()
    html = q.to_html()
    return (map(str,q.solution),html)
    

def validate(answer,sol):
    """Validate the users answer (answer) against the solution stored
       in the datastore. Note that since fractional types are not allowed
       in the datastore, it is necessary to parse both the user answer
       and the stored solution. Further, sets are used since order of
       roots (in the case of algebraic expressions) may be arbitrary."""
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


