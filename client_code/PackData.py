import anvil.facebook.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
import random
import anvil.http

#This is a module.
colors = {
  "Normal": "#A8A77A",
  "Fire": "#EE8130",
  "Water": "#6390F0",
  "Electric": "#F7D02C",
  "Grass": "#7AC74C",
  "Ice": "#96D9D6",
  "Fighting": "#C22E28",
  "Poison": "#A33EA1",
  "Ground": "#E2BF65",
  "Flying": "#A98FF3",
  "Psychic": "#F95587",
  "Bug": "#A6B91A",
  "Rock": "#B6A136",
  "Ghost": "#735797",
  "Dragon": "#6F35FC",
  "Dark": "#705746",
  "Steel": "#B7B7CE",
  "Fairy": "#D685AD"
}
# Example Usage:
# print(f"Fire type color: {pokemon_type_colors['Fire']}")
def getcolor(types):
  return colors[types[0].title()]
regions=[
  'kanto',
  'hoenn',
  'galar',
  'paldea'
]

def get_random_pokemon_from_region(region_name, count=2):
  # 1. Get region Pokedex data
  url = f"https://pokeapi.co/api/v2/pokedex/{region_name}"
  pokedex = anvil.http.request(url, json=True)

  # 2. Extract pokemon entries
  pokemon_entries = pokedex['pokemon_entries']

  # 3. Select random samples
  if count > len(pokemon_entries):
    count = len(pokemon_entries)

  selected_pokemon = random.sample(pokemon_entries, count)

  # 4. Format/Fetch details for each selected pokemon
  result = []
  for p in selected_pokemon:
    name = p['pokemon_species']['name']
    # You could call pokeapi again here for images if needed
    result.append(name)

  return result


packs={
  'fire':['charmander','charmeleon','charizard','moltres','arcanine','growlithe','entei','blaziken','ponyta','infernape','vulpix','magmar','flareon'],
  'basic':['pikachu','squirtle','charmander','ivysaur','eevee','clefairy'],
  'halloween':['murkrow','marshadow','pumpkaboo',"gengar",'banette','houndstone','dusknoir','chandelure','haunter','litwick','honchkrow','mismagius','noibat','noivern','ursaluna','ursaring','lunatone'],
  'eevee evolves':['eevee','sylveon','flareon','glaceon','vaporeon','jolteon','espeon','umbreon','leafeon'],
  'electricute':['pikachu','pichu','raichu','lenler','jolteon','zapdos','helioptile','heliolisk','dedenne','pawmot','boltund',"morpeko",'minun','plusle'],
  'grassy wonders':['golem',"sandshrew",'venusaur','bulbasaur','ivysaur','exeggutor','exeggcute','victreebel','breloom','roserade','celebi','sceptile','leafeon','ogerpon',"magikarp"],
  'water':['squirtle','wartortle','blastoise','psyduck','cloyster','gyrados','vaporeon','suicune','kingdra','palkia','lapras','greninja','kyogre','shapedo',"wooper"],
  'mighty dragons':['rayquaza',"dragonite",'garchomp','altaria','flygon','dragonair','charizard'],
  'magical':['sylveon','murkrow','marshadow','mew','mewtwo','malamar','umbreon','espeon','natu','xatu','honchkrow','houndour','houndoom','hypno','drowzee',"rapidash",'meowth',"purrloin",'slowpoke','baltoy'],
  'icy wonderland':['snorunt','glaceon','cloyster','lapras','dewgong','beartic','snom','spheal','abomasnow','sealeo','kyogre'],
  'whales':['dewgong','kyogre','wailord','wailmer','cetitan'],
  'dolphins':['kyogre','palafin','cetitan','dewgong'],
  'the army':['armarouge','falinks','zacian','zamazenta'],
  'swords and bolts':['doublade','melmetal','meltan','golurk','registeel','klink'],
  'land animalia':['mankey',"lechonk",'wooper','charmander','squirtle','sandshrew','oranguru','rattata','caterpie','eevee','meowth','growlithe','pidove','pidgeot','empoleon',"stufful"],
  "dinosaurs":['tyrantrum','bastiodon','aurorus','baxcalibur','archeops','aerodactyl',"lapras"],
  "ice cream":['vanillite','vanillish','vanilluxe'],
  'food':['vanillite','dachsbun','smoliv','tatsugiri','slurpuff','appletun','dipplin','sinistcha','scovillain','capsakid','cherubi','hydrapple','polteageist','poltchageist','barraskewda','dolliv','arboliva'],
  'pidove premium':['pidove','pidove'],
  "torchic premium":['torchic','torchic'],
  "magikarp premium":['magikarp','magikarp']
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
  for k in regions:
    x.append(k)
  return x
  
def getpack(n):
  if n in packs:
    return packs[n]
  else:
    try:
      return get_random_pokemon_from_region(n,count=10)
    except:
      return []

weaks=[
  ['grass','normal'],
  ['fire','grass'],
  ['water','fire'],
  ['electric','water'],
  ['fighting','electric'],
  ['fire',"steel"],
  ['pyschic','fighting'],
  ['dark','pyschic'],
  ['grass','fighting'],
  ['steel','fairy'],
  ['fairy','dragon'],
  ['bug','dark'],
  ["fairy","dark"],
  ['fighting','dark']
]

def resistance(x,y):
  for ix in x:
    for iy in y:
      if ix==iy:
        return -30
  return 0

def weak(x,y):
  x=x['types']
  y=y['types']
  for ix in x:
    for iy in y:
      if [ix,iy] in weaks and ix not in y:
        return 50+resistance(x,y)
  return resistance(x,y)

def reward():
  if random.randint(0,1)==1:
    # Get the current date and time
    today = datetime.now()
    # Calculate the date and time for the day before
    yesterday = today - timedelta(days=1)
    anvil.users.get_user()["last_claim"]=yesterday

"""
def get_random_pokemon_from_region(region_name, count=2):
  # 1. Get region Pokedex data
  url = f"https://pokeapi.co/api/v2/pokedex/{region_name}"
  pokedex = anvil.http.request(url, json=True)

  # 2. Extract pokemon entries
  pokemon_entries = pokedex['pokemon_entries']

  # 3. Select random samples
  if count > len(pokemon_entries):
    count = len(pokemon_entries)

  selected_pokemon = random.sample(pokemon_entries, count)

  # 4. Format/Fetch details for each selected pokemon
  result = []
  for p in selected_pokemon:
    name = p['pokemon_species']['name']
    # You could call pokeapi again here for images if needed
    result.append(name)

  return result
"""