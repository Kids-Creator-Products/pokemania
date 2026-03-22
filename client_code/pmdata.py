import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.http
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#

class Request(object):
  def get(self,x):
    return anvil.server.call_s('get',x)
  def img(self,x):
    return anvil.http.request(x)
  def file(self,x):
    return 'https://raw.githubusercontent.com/Kids-Creator-Products/projects-data/refs/heads/main/pokemania/'+x