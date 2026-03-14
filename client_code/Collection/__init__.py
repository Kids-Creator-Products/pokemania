from ._anvil_designer import CollectionTemplate
from anvil import *
import anvil.server
from routing import router
import m3.components as m3
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Collection(CollectionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    x=[]
    for i in anvil.users.get_user()['Cards']:
      x.append({'name':i})
    # Any code you write here will run before the form opens.
    self.repeating_panel_1.items=x
