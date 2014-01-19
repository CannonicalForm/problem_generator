#!/usr/bin/env python

"""
   A set of objects for other handlers to inherit from, including a jinja2
   environment, a base handler, and an extension to the dict data type,
   implimenting an extend method, similar to the list.extend method.
"""

import webapp2
import jinja2
import os
from google.appengine.api import users

td = os.path.join(os.path.dirname(__file__),'../views')
env = jinja2.Environment(loader = jinja2.FileSystemLoader(td),
                         autoescape = True)


class Handler(webapp2.RequestHandler):
    """A base handler for use across all other handlers. It sets up
       rendering, using jinja2, as well as creating contexts that are
       useful for all handlers, such as a login-url and logout-url."""
    def __init__(self,*args,**kwargs):
        super(Handler,self).__init__(*args,**kwargs)
        self.login_url = users.create_login_url(self.request.path)
        self.logout_url = users.create_logout_url(self.request.path)
        self.context = Extensible()
        self.context = self.context.extend({'login_url': self.login_url,
                                            'logout_url':self.logout_url})
        
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t = env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))



class Extensible(dict):
    """Basically impliment the list.extend method for dictionaries,
       with one caveat: key's already in the dict will not be
       overwritten."""
    def extend(self,d):
        """While counterintuitive, this is a returnable function so
           that when context's are updated, they are atomic between
           GET and POST methods, which may (and probably will) require
           a different set of values for the same variables."""
        for key,val in d.iteritems():
            if key in self.keys():
                continue
            else:
                self[key] = val
        return self
