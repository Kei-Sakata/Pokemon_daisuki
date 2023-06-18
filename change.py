from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.config import Config
from kivy.uix.filechooser import FileChooserListView 
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '480')
 
class Display(BoxLayout):
    pass
class Screen_One(Screen):
    pass
 
class Screen_Two(Screen):
    pass
class Screen_Three(Screen):
    pass
class Screen_Four(Screen):
    pass
class TestFileChooser(App):
    def build(self):
        return RootWidget() 
class CHANGEApp(App):
    def build(self):
        return Display()
 
if __name__ == '__main__':
    CHANGEApp().run()
