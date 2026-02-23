from ._anvil_designer import PacksTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import PackData


class Packs(PacksTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
  def refresh(self):
    x=[]
    y=PackData.getpacknames()
    for i in y:
      z=PackData.getpack(i)
      x.append({'name':i,'data':z})
    self.repeating_panel_1.items=x
    # Any code you write here will run before the form opens.
