import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#

packs={
  'fire':['charmander','charmeleon','charizard','moltres','arcanine','growlithe','entei','blaziken','ponyta','infernape','vulpix','magmar','flareon'],
  'basic':['pikachu','squirtle','charmander','ivysaur','eevee','clefairy'],
  'halloween':['murkrow','marshadow','pumpkaboo'],
  'eevee evolves':['eevee','sylveon','flareon','glaceon','vaporeon','jolteon','espeon','umbreon','leafeon']
}

def getlastclaim():
  return anvil.users.get_user()['last_claim']
def canclaim():
  try:
    x=getlastclaim().hour 
    return datetime.now().hour!=x
  except:
    return True
def getpacknames():
  x=[]
  for k in packs:
    x.append(k)
  return x
def getpack(n):
  return packs[n]