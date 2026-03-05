import anvil.facebook.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
# This is a module.

packs={
  'fire':['charmander','charmeleon','charizard','moltres','arcanine','growlithe','entei','blaziken','ponyta','infernape','vulpix','magmar','flareon'],
  'basic':['pikachu','squirtle','charmander','ivysaur','eevee','clefairy'],
  'halloween':['murkrow','marshadow','pumpkaboo',"gengar",'banette','houndstone','dusknoir','chandelure','haunter','litwick','honchkrow','mismagius','noibat','noivern','ursaluna','ursaring','lunatone'],
  'eevee evolves':['eevee','sylveon','flareon','glaceon','vaporeon','jolteon','espeon','umbreon','leafeon'],
  'electricute':['pikachu','pichu','raichu','lenler','zolteon','zapdos','helioptile','heliolisk','dedenne','pawmot','boltund',"morpeko",'minun','plusle'],
  'grassy wonders':['golem',"sandshrew",'venusaur','bulbasaur','ivysaur','exeggutor','exeggcute','victreebel','breloom','roserade','celebi','sceptile','leafeon','ogerpon',"magikarp"],
  'water':['squirtle','wartortle','blastoise','psyduck','cloyster','gyrados','vaporeon','suicune','kingdra','palkia','lapras','greninja','kyogre','shapedo'],
  'mighty dragons':['rayquaza',"dragonite",'garchomp','altaria','flygon','dragonair','charizard'],
  'magical':['sylveon','murkrow','marshadow','mew','mewtwo','malamar','umbreon','espeon','natu','xatu','honchkrow','houndour','houndoom','hypno','drowzee',"rapidash",'meowth',"purrloin",'slowpoke','baltoy'],
  'icy wonderland':['snorunt','glaceon','cloyster','lapras','dewgong','beartic','snom','spheal','abomasnow','sealeo','kyogre'],
  'whales':['dewgong','kyogre','wailord','wailmer','cetitan'],
  'dolphins':['kyogre','palafin','cetitan','dewgong'],
  'the army':['armarouge','falinks','zacian','escavalier']
}

def getlastclaim():
  if anvil.users.get_user()['last_claim']:
    return anvil.users.get_user()['last_claim']
  else:
    anvil.users.get_user()['last_claim']=datetime.now()
    return datetime.now()
def canclaim():
  if True:
    now=datetime.now()
    provided_date=getlastclaim()
    return provided_date.strftime("%Y-%m-%d %H") != now.strftime("%Y-%m-%d %H")
def getpacknames():
  x=[]
  for k in packs:
    x.append(k)
  return x
def getpack(n):
  return packs[n]

weaks=[
  ['grass','normal'],
  ['fire','grass'],
  ['water','fire'],
  ['electric','water'],
  ['fighting','electric'],
  ['steel','fire'],
  ['pyschic','fighting'],
  ['dark','pyschic'],
  ['electric','fighting']
]

def weak(x,y):
  x=x['types']
  y=y['types']
  for ix in x:
    for iy in y:
      if [ix,iy] in weaks:
        return 30
  return 0