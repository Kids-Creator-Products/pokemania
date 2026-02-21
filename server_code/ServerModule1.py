import anvil.server
import requests
@anvil.server.callable
def getpower(url):
  x=requests.get(url)
  if x.status_code==200:
    y=x.json()
    return str(y.get('power','0'))
  else:
    return ''
@anvil.server.callable
def get_pokemon_details(name):
  # Full API endpoint URL for this specific Pokémon
  api_url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
  response = requests.get(api_url)

  if response.status_code == 200:
    data = response.json()
    return {
      'api_url': api_url,
      'name': data['name'].capitalize(),
      'image': data['sprites']['front_default'],
      # Extract names from the 'moves' list
      'attacks': [m['move']['name'].replace('-', ' ').title()+'-'+getpower(m['move']['url']) for m in data['moves']],
      'types': [t['type']['name'] for t in data['types']]
    }
  return None
