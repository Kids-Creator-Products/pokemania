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
from .. import Websocket

class Cards(CardsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.last=properties.get('last',False)
    try:
      x=anvil.users.get_user()['Cards']
    except:
      self.button_2_click()
      x=anvil.users.get_user()["Cards"]
      if not x:
        anvil.users.get_user()['Cards']=[]
        anvil.js.window.location.reload()
    y={}
    for i in x:
      if i in y:
        y[i]+=1
      else:
        y[i]=1
    z=[i+'-'+str(y[i]) for i in y]
    self.retreat=True
    self.drop_down_1.items=z
    try:
      self.text_box_1.text=properties.get('battle','')
      if 'battle' in properties:
        self.retreat=False
    except:
      pass
    self.text_box_1.text=Websocket.getFor()
    c=PackData.canclaim()
    self.navigation_link_1.badge=c
    if c:
      Websocket.trade()
    if not self.retreat:
      self.text_box_1.hide_text=True
      x=Notification('Choose a pokemon to send in!',title='Battle!',timeout=5)
      x.show()
    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    x=self.drop_down_1.selected_value.split("-")[0]
    y=anvil.server.get_app_origin('published')+'/pokemon/'+x
    try:
      if anvil.confirm('Redirect?'):
        anvil.js.window.location.replace(y)
    except:
      pass
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
    if self.last:
      uri+='#last'
    #anvil.js.window.location.href=uri
    #open_form('Battle',battle=c1,bad=c2)
    x=Link(url=uri,text='Battle!')
    if not self.retreat:
      x.add_event_handler('click',self.clear)
    self.add_component(x)
    #self.sound('ThemeMusic/Battle.m4a')

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    if anvil.users.login_with_form(allow_cancel=True):
      pass
      if not anvil.users.get_user(allow_remembered=True)['Cards']:
        anvil.users.get_user()['Cards']=[]
  def sound(self,name='punch.mp3'):
    #try:
    #  self.audio_element.stop()
    #except AttributeError:
     # pass
    audio_url = "/_/theme/"+name #Or use a URL from a Media object
    self.audio_element = anvil.js.window.Audio(audio_url)
    self.audio_element.play()

  @handle("drop_down_1", "change")
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    #self.sound()
    pass

  @handle("button_3", "click")
  def button_3_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.evolvable(False)
    x=self.drop_down_1.selected_value.split('-')
    c=x[0]
    if int(x[1])>1:
      if True:
        into=anvil.server.call_s('get_next_evolution',c)
      #except:
      #  return
      owned=anvil.users.get_user()['Cards']
      if 'Final' in into:
        alert('Cancelled.')
        self.evolvable()
        return
      if c in owned:
        for i in range(2):
          try:
            owned.remove(c)
          except:
            pass
      owned.append(into)
      anvil.users.get_user()['Cards']=owned
      self.evolvable()
      anvil.js.window.location.reload()
    else:
      self.evolvable()
  def evolvable(self,val=True):
    self.button_3.enabled=val
  @handle("button_4", "click")
  def button_4_click(self, **event_args):
    """This method is called when the component is clicked."""
    open_form('Credits')

  @handle("button_5", "click")
  def button_5_click(self, **event_args):
    """This method is called when the component is clicked."""
    if confirm('Offer card? Cancel to clear current offer.'):
      Websocket.setoffer(self.drop_down_1.selected_value,self.text_box_1.text)
    else:
      Websocket.setoffer(None,None)
