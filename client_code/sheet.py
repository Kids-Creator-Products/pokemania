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
  """
def backusr(usr):
  db=app_files.users['usr']
  for i in db.rows:
    if i['email']==usr:
      i.delete()
  d=anvil.users.get_user()
  x={}
  for k in d:
    x[k]=str(d[k])
  db.add_row(x)
  """
def backusr(usr_email):
  # 1. Get the current logged-in user
  user = anvil.users.get_user()
  if not user:
    return "No user logged in"

    # 2. Reference your storage table
  db = app_files.users['usr'] #Assuming 'users' is an Anvil Data Table

  # 3. Look for an existing record
  try:
    db.list_rows(email=anvil.users.get_user()['email'])[0].delete()
  except:
    pass

  # 4. Prepare data (converting to string as you did)
  x=['email','Cards','fav','Offer','For','msg']
  user_data = {k: str(user[k]) for k in x}

  db.add_row(**user_data)
def fixtype(v):
  try:
    return eval(v)
  except:
    return v
def reload_sheet():
  try:
    x=app_files.users['usr'].list_rows(email=anvil.users.get_user()['email'])[0]
  except:
    return
  for k in x:
    if k!='email':
      v=x[k]
      anvil.users.get_user()[k]=fixtype(v)