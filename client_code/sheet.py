import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#

def getusrs():
  return app_files.users['usr'].rows
def backusr(usr):
  db=app_files.users['usr']
  for i in getusrs():
    if i['email']==usr:
      i.delete()
  d=app_tables.users.get(email=usr)
  x={}
  for k in d:
    x[k]=d[k]
  db.add_row(x)