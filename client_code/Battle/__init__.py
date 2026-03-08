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
import anvil.js
from .. import PackData

class Battle(BattleTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.hp=[500,500]
    self.init_components(**properties)
    self.atk=0
    self.res=0
    self.data={}
    try:
      self.data=anvil.server.startup_data
    except:
      self.data={}
    if "battle" in properties:
      self.data['battle']=properties['battle']
      self.data['bad']=properties['bad']
    try:
      if self.data['battle'].lower().strip() in anvil.users.get_user()['Cards'] or True:
        self.playerdata=anvil.server.call('get_pokemon_details',self.data['battle'])
      self.enemydata=anvil.server.call('get_pokemon_details',self.data['bad'])
    except:
      anvil.js.window.location.reload()
    try:
      self.image_1.source=self.enemydata['image']
      self.image_2.source=self.playerdata['image']
    except:
      pass
    self.ismyturn=random.choice([False,True])
    self.canuseitem=self.ismyturn
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
        self.hp[0]-=max(y)+PackData.weak(self.enemydata,self.playerdata)-self.res
      except:
        pass
      #x=Audio(self.playerdata['sound'])
      #x.play()
      self.icon_button_1.enabled=True
      self.res,self.canuseitem=0,True
      self.ismyturn=True
    if self.hp[0]<1 or self.hp[1]<1:
      self.clear()
      if self.hp[0]<1:
        t="DEFEAT!"
        if confirm('Retreat?'):
          open_form('Cards',battle=self.data['bad'])
        else:
          self.sound('Doubt.m4a')
      else:
        t="VICTORY!"
        self.sound('B-Day.m4a')
        if anvil.get_url_hash()=='last':
          PackData.reward()
        else:
          open_form('Cards',battle=self.data['bad'],last=True)
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
        self.hp[1]-=y+PackData.weak(self.playerdata,self.enemydata)+self.atk
        self.atk=0
        self.ismyturn=False
        x=Audio(self.enemydata['sound'])
        x.play()
  def sound(self,surl='punch.mp3'):
    sound_url = anvil.server.get_app_origin('published')+'/_/theme/'+surl
    my_sound = Audio(sound_url)
    my_sound.play()

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    if self.ismyturn:
      self.atk=0
      self.ismyturn=False

  @handle("dropdown_menu_2", "change")
  def dropdown_menu_2_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.canuseitem and self.ismyturn:
      x=self.dropdown_menu_2.selected_value.lower()
      if x=='potion':
        self.hp[0]=min([self.hp[0]+30,self.playerdata['health']])
      if x=='sword':
        self.atk=40
      if x=='armor':
        self.res=50
      else:
        return
      self.canuseitem=False
