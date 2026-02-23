from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import PackData
from datetime import datetime

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    buttonx=[
      ('More Info','info'),
      ('OK','cancel')
    ]
    if PackData.canclaim():
      anvil.server.call('addPack',self.item['data'])
      x=alert('Pack claimed',buttons=buttonx)
      anvil.users.get_user()['last_claim']=datetime.now()
    else:
      x=alert('Could not claim.',buttons=buttonx)
    if x=='info':
      alert('You can only open a pack every hour, each pack is usually two cards.',buttons=[('OK','cancel')])

