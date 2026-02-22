from ._anvil_designer import Form1Template
from anvil import *
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set up the form and its initial state
    self.init_components(**properties)
    self.update()
    self.text_box_search.text=anvil.server.startup_data.get("pokemon")
  @handle('button_search','click')
  def button_search_click(self, **event_args):
    """This method is called when the search button is clicked"""
    # 1. Clear previous data and show 'Searching...' status
    self.label_info.text = "Searching..."
    self.image_pokemon.source = None
    self.text_area_moves.text = ""
    self.label_url.text = ""

    pokemon_name = self.text_box_search.text.lower().strip()

    # 2. Call the Server Module function
    # Ensure your Server Module has a function decorated with @anvil.server.callable
    pokemon_data = anvil.server.call('get_pokemon_details', pokemon_name)

    if pokemon_data:
      # 3. Display Basic Info
      self.label_info.text = f"Name: {pokemon_data['name']}\nTypes: {','.join(pokemon_data['types'])}\n{str(pokemon_data['health'])} HP"

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

  @handle("text_box_search", "pressed_enter")
  def text_box_search_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form(allow_cancel=True)
    try:
      anvil.users.get_user()['Cards']=[]
      anvil.users.get_user()['Potential']=0
    except:
      pass
  def update(self):
    self.rich_text_1.content=anvil.users.get_user()['Potential']
    y=anvil.users.get_user()['Potential']
    y=y-y%0.1
    anvil.users.get_user()['Potential']=y
  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.get_user()['Potential']+=0.1
    if anvil.users.get_user()['Potential']%1==0:
      x=anvil.users.get_user()['Cards']
      x.append(self.text_box_search.text.lower().strip())
      anvil.users.get_user()['Cards']=x
      anvil.users.get_user()['Potential']=0.1
      anvil.alert('Card has been added.')
    #anvil.users.get_user()['Potential']+=0.1
    self.update()
    
