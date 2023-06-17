
# 画面の縦・横のサイズを指定
from kivy.config import Config
Config.set('graphics','width','640')
Config.set('graphics','height','480')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from random import randint

class ImageWidget(Widget):#Image Widgetというアプリ
    source = StringProperty('./img/0.jpg')

    def __init__(self, **kwargs):
        super(ImageWidget, self).__init__(**kwargs)
        pass

    def btn_first(self):
        self.source='./img/0.jpg'

    def btn_rand(self):
        self.source = './img/'+f'{randint(0,1)}.jpg'

class ImageApp(App):#ImageAppのImage とkvファイルの名称を合わせる必要がある。今回はimage.kv
    def __init__(self, **kwargs):
        super(ImageApp,self).__init__(**kwargs)
        self.title = '画像表示'
    pass

if __name__ == '__main__':
    ImageApp().run()
