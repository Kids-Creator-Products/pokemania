from ._anvil_designer import CardTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import PackData

class Card(CardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.navigation_link_1.visible=self.navlink
    if False:
      self.data=properties
    else:
      self.data=anvil.server.startup_data
    self.n=self.data['name']
    if self.name and self.name!='':
      self.n=self.name
    self.x=anvil.server.call('get_pokemon_details',self.n)
    # Any code you write here will run before the form opens.
    self.heading_1.text=self.x['name']+'      '+str(self.x['health'])+' HP              '+self.x['types'][0]
    self.image_1.source=self.x["image"]
    self.rich_text_1.content="<br/>".join([i.title() for i in self.x['attacks']])

    c=PackData.colors[self.x['types'][0].title()]
    self.content_panel.background=c
    self.heading_1.background_color=c
    self.image_1.background=c
    self.heading_1.text_color='white'
