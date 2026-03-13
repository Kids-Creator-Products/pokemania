from ._anvil_designer import PacksTemplate
from anvil import *
from routing import router
import anvil.facebook.auth
import anvil.server
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
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
      if i in PackData.regions:
        i=i+' Region'
      if len(z)>0:
        x.append({'name':i,'data':z})
    self.repeating_panel_1.items=x
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    if PackData.canclaim():
      self.button_1.enabled=False
      anvil.server.call('addCard',self.text_area_1.text)
      anvil.users.get_user()['last_claim']=datetime.now()
      self.button_1.enabled=True
    else:
      alert("You can't get a pack now.")
