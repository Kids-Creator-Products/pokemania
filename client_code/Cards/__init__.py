from ._anvil_designer import CardsTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js


class Cards(CardsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    x=anvil.users.get_user()['Cards']
    y={}
    for i in x:
      if i in y:
        y[i]+=1
      else:
        y[i]=1
    z=[i+'-'+str(y[i]) for i in y]
    self.drop_down_1.items=z
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    x=self.drop_down_1.selected_value.split("-")[0]
    y=anvil.server.get_app_origin('published')+'/pokemon/'+x
    z=Link(url=y,text='Open me to enter!')
    self.content_panel.add_component(z)