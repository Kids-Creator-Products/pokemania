from ._anvil_designer import CardsTemplate
from anvil import *
import anvil.facebook.auth
import m3.components as m3
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from .. import PackData


class Cards(CardsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      x=anvil.users.get_user()['Cards']
    except:
      self.button_2_click()
    y={}
    for i in x:
      if i in y:
        y[i]+=1
      else:
        y[i]=1
    z=[i+'-'+str(y[i]) for i in y]
    self.drop_down_1.items=z
    c=PackData.canclaim()
    self.navigation_link_1.badge=c
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    x=self.drop_down_1.selected_value.split("-")[0]
    y=anvil.server.get_app_origin('published')+'/pokemon/'+x
    z=Link(url=y,text='Open me to enter!')
    self.content_panel.add_component(z)

  @handle("text_box_1", "pressed_enter")
  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    pass

  @handle("icon_button_1", "click")
  def icon_button_1_click(self, **event_args):
    c1=self.drop_down_1.selected_value.split('-')[0]
    c2=self.text_box_1.text
    uri=anvil.server.get_app_origin('published')+'/battle/'+c1+'/'+c2
    x=Link(url=uri,text='Battle!')
    self.add_component(x)

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.users.login_with_form(allow_cancel=True)
