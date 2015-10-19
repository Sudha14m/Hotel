#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import cgi
from google.appengine.ext import ndb
from google.appengine.api import users
import traceback
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Person(ndb.Model):
    username = ndb.StringProperty(indexed =False)
    password = ndb.StringProperty(indexed = False)
    semail = ndb.StringProperty(indexed = True)
    type = ndb.StringProperty(indexed = False)


class LoginController(webapp2.RequestHandler):
    def post(self):
        self.response.write("hii")
        user = users.get_current_user()
        if user:
            q = Person.query(Person.semail!= None).count()
            template=None
            if q is not 0:
                Person(username=self.request.post('username'),semail=user.email,password=self.request.post('password'),
                       type="user").put()
                template=JINJA_ENVIRONMENT.get_template('/www/users.html')
                self.response.write(template.render())
            else:
                 Person(username=self.request.post('username'),semail=user.email,password=self.request.post('password'),
                        type="admin").put()
                 template=JINJA_ENVIRONMENT.get_template('/www/adminpage.html')
                 self.response.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get(self):
        self.response.write("hii")


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            self.response.write('Hello, ' + user.nickname())
            q1 = Person.query(Person.semail==user.email()).get()
            if q1 is None:
              #  template = JINJA_ENVIRONMENT.get_template('/www/index.html')
                template = JINJA_ENVIRONMENT.get_template('/index1.html')

                self.response.write(template.render())
            else:
                if q1.type == 'admin':
                    template = JINJA_ENVIRONMENT.get_template('/www/adminhome.html')
                    self.response.write(template.render())
                else:
                    template = JINJA_ENVIRONMENT.get_template('/www/users.html')
                    self.response.write(template.render())

        else:
            self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index', LoginController)
], debug=True)