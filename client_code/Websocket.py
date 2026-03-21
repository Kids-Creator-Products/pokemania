import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#

def setproperty(x,y):
  anvil.users.get_user()[x]=y

def setoffer(x,y):
  setproperty('Offer',x)
  setproperty('For',y)

def switch(w,y):
  w=w.split('-')[0]
  x=anvil.users.get_user()['Cards']
  x.remove(w)
  setproperty('Cards',x)
  anvil.server.call_s('addCard',y)
  setoffer(None,None)

def trade(usr=None):
  x=anvil.users.get_user()
  if usr:
    x=app_tables.users.get(email=usr)
    if not x:
      return
  if random.randint(1,3)==2 or usr:
    try:
      if x['Offer'] in anvil.users.get_user()['Cards']:
        switch(x['Offer'],x['For'])
    except:
      pass

def getFor():
  return anvil.users.get_user()['For']

def getmsg():
  r=anvil.users.get_user()['msg']
  if not r:
    return []
  return r

def sendmsg(usr,msg):
  d=app_tables.users.get(email=usr)
  if not d:
    return False
  d=d['msg']
  if not d:
    d=[]
  if 'trade' in msg and 'Chat:'+usr+':trade' in getmsg():
    trade(usr)
  d.append(msg)
  return True