import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import requests

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


@anvil.server.callable
def get_pokemon_details(name):
  # Full API endpoint URL for this specific Pokémon
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
      'name': data['name'].capitalize(),
      'image': data['sprites']['front_default'],
      # Extract names from the 'moves' list
      'attacks': [m['move']['name'].replace('-', ' ').title()+'-'+getpower(m['move']['url']) for m in data['moves']],
      'types': [t['type']['name'] for t in data['types']],
      'health':hp
    }
  return None

@anvil.server.route('/pokemon/:name')
def pokemon(name):
  return anvil.server.AppResponder(data={'pokemon':name}).load_form('Form1')
@anvil.server.route("/cards")
def cards():
  return anvil.server.FormResponse('Cards')