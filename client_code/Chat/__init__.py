from ._anvil_designer import ChatTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Websocket

class Chat(ChatTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_box_1.text=''
    #self.text_box_2.hide_text=True
    self.refresh()
    self.text_box_1
    # Any code you write here will run before the form opens.
  def refresh(self):
    x=Websocket.getmsg()
    y=[]
    for i in x:
      if i[:5]=='Chat:':
        y.append(i[5:])
    self.rich_text_1.content='\n'.join(y)
  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    x=self.text_box_1.text
    u=self.text_box_2.text
    Websocket.sendmsg(u,'Chat:'+anvil.users.get_user()['email']+':'+x)
    self.refresh()
