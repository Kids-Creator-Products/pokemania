import anvil.files
from anvil.files import data_files
import anvil.secrets
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import requests
import random
import datetime
import Custom

@anvil.server.callable
def get_pokemon_ids(name):
  # PokéAPI uses 'species' to group all variants (Mega, Gmax, etc.)
  url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}/"

  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # 'varieties' contains the specific IDs for each form
    varieties = data.get('varieties', [])

    results = {}
    for v in varieties:
      v_name = v['pokemon']['name']
      # The ID is the last numeric part of the URL
      v_id = v['pokemon']['url'].strip('/').split('/')[-1]
      results[v_name] = v_id

    return results

  except requests.exceptions.RequestException as e:
    return f"Error fetching data: {e}"

# Example for Charizard (includes Mega X, Mega Y, and Gmax/VMAX)
pokemon_name = "kyogre"
ids = get_pokemon_ids(pokemon_name)
print(ids)


def fixattack(atk):
  y=atk.split('-')
  if 'none' in atk.lower():
    y[1]='0'
  return '-'.join(y)


def get_desc(url):
  move_url=url
  move_response = requests.get(move_url)
  move_response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
  move_data = move_response.json()

  #.  2. Extract the 'flavor_text_entries'
  flavor_text_entries = move_data.get("flavor_text_entries", [])

  # 3. Iterate through the entries to find the English description
  for entry in flavor_text_entries:
    if entry["language"]["name"] == "en":
      # Return the first English entry found
      return entry["flavor_text"].replace('\n', ' ')

  print(f"No English description found for move '{move_name}'.")
  return None

@anvil.server.callable
def getpower(url):
  x=requests.get(url)
  if x.status_code==200:
    y=x.json()
    if True:
      z=get_desc(url)
      if not z:
        z=''
    return str(y.get('power','0'))+'-'+z
  else:
    return ''

evolution={
  'eevee':["sylveon",'umbreon','espeon','flareon','vaporeon','jolteon','glaceon','leafeon']
}
    
@anvil.server.callable
def get_next_evolution(pokemon_name):
  # 1. Get species data to find evolution chain URL
  if pokemon_name in evolution:
    return random.choice(evolution[pokemon_name])
  species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"
  try:
    species_data = requests.get(species_url).json()
  except:
    return 'Final'
  evolution_chain_url = species_data['evolution_chain']['url']

  # 2. Get the evolution chain data
  chain_data = requests.get(evolution_chain_url).json()
  chain = chain_data['chain']

  # 3. Traverse the chain (Basic example)
  # Find current pokemon in chain, then look at next evolves_to
  current_node = chain
  while current_node['species']['name'] != pokemon_name.lower():
    if not current_node['evolves_to']:
      return "Final"
    current_node = current_node['evolves_to'][0]

    # Return next evolution
  if current_node['evolves_to']:
    return current_node['evolves_to'][0]['species']['name']
  else:
    return "Final Evolution"
# Example usage
#print(get_next_evolution("charmeleon")) # Output: charizard
"""
@anvil.server.callable
def get_next_evolution(pokemon_name):
  pokemon_name = pokemon_name.lower().strip()
  species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/"
  try:
    species_data = requests.get(species_url).json()
    evolution_chain_url = species_data['evolution_chain']['url']
    chain_data = requests.get(evolution_chain_url).json()
  except:
    return "Final"

  def find_next(node, target):
    # If this node is the one we're looking for
    if node['species']['name'] == target:
      if node['evolves_to']:
        # Return the name of the first available evolution
        return node['evolves_to'][0]['species']['name'].capitalize()
      return "Final Evolution"

      # If not, check all possible branches (for Eevee, etc.)
    for evolution in node['evolves_to']:
      result = find_next(evolution, target)
      if result:
        return result
    return None

  result = find_next(chain_data['chain'], pokemon_name)
  return result if result else "Final Evolution"
"""
"""
@anvil.server.callable
def get_next_evolution(pokemon_name):
  pokemon_name = pokemon_name.lower().strip()
  species_url = f"https://pokeapi.co{pokemon_name}/"

  try:
    species_data = requests.get(species_url).json()
    chain_url = species_data['evolution_chain']['url']
    chain_data = requests.get(chain_url).json()
  except:
    return "Final"

  def find_target_node(node, target):
    # 1. Is this the Pokémon we are looking for?
    if node['species']['name'] == target:
      return node

      # 2. If not, check all its possible evolutions
    for evolution in node['evolves_to']:
      found = find_target_node(evolution, target)
      if found:
        return found
    return None

    # Start searching from the base of the chain (e.g., Charmander)
  target_node = find_target_node(chain_data['chain'], pokemon_name)

  if target_node and target_node['evolves_to']:
    # Return the first evolution found in the list
    return target_node['evolves_to'][0]['species']['name'].capitalize()

  return "Final Evolution"
"""
"""
@anvil.server.callable
def get_next_evolution(pokemon_name):
  name = pokemon_name.lower().strip()
  try:
    # 1. Get species to find the chain URL
    species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}/").json()
    chain_data = requests.get(species['evolution_chain']['url']).json()

    # 2. Start searching from the base of the chain
    return search_tree(chain_data['chain'], name)
  except:
    return "Final Evolution"
"""
def search_tree(node, target):
  # Is THIS the pokemon?
  if node['species']['name'] == target:
    if node['evolves_to']:
      # Return the first available evolution
      return node['evolves_to'][0]['species']['name'].capitalize()
    return "Final Evolution"

    # If not, check every branch (e.g., Eevee's 8 paths)
  for next_node in node['evolves_to']:
    found = search_tree(next_node, target)
    if found:
      return found

  return None


@anvil.server.callable
def get_pokemon_details(name):
  # Full API endpoint URL for this specific Pokémon
  if name.endswith('max') or name.endswith('x') or name.endswith('y'):
    ids=get_pokemon_ids('-'.join(name.split('-')[:-1]))
    name=str(ids[name])
  """if False:
    customs=requests.get('https://raw.githubusercontent.com/cool-guys-bfc2/custom-pokemon/refs/heads/main/cards/cards.json').json()
    if name+'.json' in customs:
      card=requests.get('https://raw.githubusercontent.com/cool-guys-bfc2/custom-pokemon/refs/heads/main/cards/custom/{x}.json'.replace('{x}',name)).json()
      card['image']='https://raw.githubusercontent.com/cool-guys-bfc2/custom-pokemon/refs/heads/main/cards/images/'+name+'.png'
      return card"""
  #return Custom.cards[name]
  #except:
  #pass
  api_url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
  response = requests.get(api_url)
  if response.status_code == 200:
    data = response.json()
    for stat_entry in data['stats']:
      if stat_entry['stat']['name'] == 'hp':
        base_hp = stat_entry['base_stat']
        #print(f"The base HP for {name.capitalize()} is: {base_hp}")
        hp=base_hp
    return {
      'api_url': api_url,
      'name': data['name'].replace('-',' ').title(),
      'image': data['sprites']['front_default'],
      # Extract names from the 'moves' list
      'attacks': [fixattack(m['move']['name'].replace('-', ' ').title()+'-'+getpower(m['move']['url'])) for m in data['moves'][:8]],
      'types': [t['type']['name'] for t in data['types']],
      'health':hp,
      'sound':data['cries'].get('latest','')
    }
  return None
  
@anvil.server.callable
def addCard(rn):
  n=rn.lower().strip()
  x=anvil.users.get_user()['Cards']
  x.append(n)
  anvil.users.get_user()['Cards']=x
#l is list of available cards, a is amount of cards.

@anvil.server.callable
def addPack(li,a=2):
  for i in range(a):
    x=random.choice(li)
    addCard(x)
    li.remove(x)

@anvil.server.route('/pokemon/:name')
def pokemon(name):
  return anvil.server.AppResponder(data={'name':name}).load_form('Card')
  
@anvil.server.route("/cards")
def cards():
  return anvil.server.FormResponse('Cards')

#@anvil.server.route('/card/:n')
def card(n):
  return anvil.server.AppResponder(data={'name':n}).load_form('Card')


@anvil.server.route('/battle/:c/:o')
def battle(c,o):
  return anvil.server.AppResponder(data={'battle':c,'bad':o}).load_form('Battle')

@anvil.server.callable
def get(x):
  return requests.get(x).text