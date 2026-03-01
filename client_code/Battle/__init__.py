from ._anvil_designer import BattleTemplate
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
import random
from anvil.js.window import Audio


class Battle(BattleTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.hp=[500,500]
    self.init_components(**properties)
    self.data=anvil.server.startup_data
    if self.data['battle'].lower().strip() in anvil.users.get_user()['Cards'] or True:
      self.playerdata=anvil.server.call('get_pokemon_details',self.data['battle'])
    self.enemydata=anvil.server.call('get_pokemon_details',self.data['bad'])
    self.image_1.source=self.enemydata['image']
    self.image_2.source=self.playerdata['image']
    self.ismyturn=random.choice([False,True])
    self.e=[0,0]
    self.hp=[self.playerdata['health'],self.enemydata['health']]
    # Any code you write here will run before the form opens.
  def getenergies(self,a):
    return round(a/60)
  def getdata(self,atk):
    return atk.split('-')
  @handle("timer_1", "tick")
  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    if not self.ismyturn and self.hp[0]>0 and self.hp[1]>0:
      self.e[1]+=1
      a=[i for i in self.enemydata['attacks'] if i is not None]
      try:  
        x=[int(self.getdata(atk)[1]) for atk in a if self.getdata()[1] not in ['None',None]]
      except:
        x=[]
        for i in a:
          try:
            x.append(int(self.getdata(i)[1]))
          except:
            pass
      y=[i for i in x if self.getenergies(i)<=self.e[1]]
      try:
        self.hp[0]-=max(y)
      except:
        pass
      #self.sound()
      self.icon_button_1.enabled=True
      self.ismyturn=True
    if self.hp[0]<1 or self.hp[1]<1:
      self.clear()
      if self.hp[0]<1:
        t="DEFEAT!"
      else:
        t="VICTORY!"
      print(t)
      t="**"+t+"**"
      x=RichText(content=t,format='markdown')
      self.add_component(x)
    self.dropdown_menu_1.items=self.playerdata['attacks']
    self.refresh_data_bindings()

  @handle("icon_button_1", "click")
  def icon_button_1_click(self, **event_args):
    self.e[0]+=1
    self.icon_button_1.enabled=False

  @handle("dropdown_menu_1", "change")
  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.ismyturn:
      x=self.dropdown_menu_1.selected_value
      y=int(self.getdata(x)[1])
      if self.getenergies(y)<=self.e[0]:
        self.hp[1]-=y
        self.ismyturn=False
        self.sound()
  def sound(self):
    sound_url = anvil.server.get_app_origin('published')+'/_/theme/punch.mp3'
    my_sound = Audio(sound_url)
    my_sound.play()