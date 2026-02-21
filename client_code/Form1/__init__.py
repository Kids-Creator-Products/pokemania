from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set up the form and its initial state
    self.init_components(**properties)
  @handle('button_search','click')
  def button_search_click(self, **event_args):
    """This method is called when the search button is clicked"""
    # 1. Clear previous data and show 'Searching...' status
    self.label_info.text = "Searching..."
    self.image_pokemon.source = None
    self.text_area_moves.text = ""
    self.label_url.text = ""

    pokemon_name = self.text_box_search.text

    # 2. Call the Server Module function
    # Ensure your Server Module has a function decorated with @anvil.server.callable
    pokemon_data = anvil.server.call('get_pokemon_details', pokemon_name)

    if pokemon_data:
      # 3. Display Basic Info
      self.label_info.text = f"Name: {pokemon_data['name']}\nTypes: {', '.join(pokemon_data['types'])}"

      # 4. Display Sprite Image
      self.image_pokemon.source = pokemon_data['image']

      # 5. Display Full API URL (Set text and optional clickable URL)
      self.label_url.text = pokemon_data['api_url']

      # 6. Display Attacks in the TextArea
      # Joins the list of moves into a single string with new lines
      self.text_area_moves.text = "\n".join(pokemon_data['attacks'])
    else:
      # Handle cases where the Pokémon is not found
      self.label_info.text = f"Error: '{pokemon_name}' not found in the PokéAPI."
      self.label_url.text = ""
