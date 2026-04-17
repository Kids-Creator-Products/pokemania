from ._anvil_designer import SearchTemplate
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

class Search(SearchTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    name=self.text_box_1.text.lower().strip()
    t=''
    try:
      x=anvil.server.call_s('get_pokemon_ids',name)
    except:
      t='This is not a valid pokemon...'
      return
    i=[]
    for k in x:
      t+='\n'+k
      v=x[k]
      c=Button(text="View Card "+k)
      def e(**kwargs):
        return anvil.open_form("Card",name=str(v))
      c.add_event_handler('click',e)
      e=None
      i.append({"val":v})
    self.repeating_panel_1.items=i
    self.rich_text_1.content=t
