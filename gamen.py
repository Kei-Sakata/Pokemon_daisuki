from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
import emo

import os
import cv2
import numpy as np
import pikapika
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.clock import Clock
from kivy.graphics.texture import Texture

class Screen_One(Screen):
    def __init__(self, **kwargs):
        super(Screen_One, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="menyu")
        button1 = Button(text="Go to masku", on_release=self.switch_to_screen_two)
        button2 = Button(text="Go to emo", on_release=self.switch_to_screen_three)
        layout.add_widget(label)
        layout.add_widget(button1)
        layout.add_widget(button2)
        self.add_widget(layout)

    def switch_to_screen_two(self, *args):
        app = App.get_running_app()
        app.root.current = 'screen_two'

    def switch_to_screen_three(self, *args):
        app = App.get_running_app()
        app.root.current = 'screen_three'


#画像ボタンクラス
class MyButton(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        #画像ボタンの画像名を格納
        self.source = kwargs["source"]
        #画像を編集できるようにテクスチャーとして扱う
        self.texture = self.button_texture(self.source)

    # トグルボタンの状態、状態によって画像が変化する
    def on_state(self, widget, value):
        if value == 'down':
            self.texture = self.button_texture(self.source, off=True)
        else:
            self.texture = self.button_texture(self.source)

    # 画像を変化させる、押した状態の時に矩形+色を暗く
    def button_texture(self, data, off=False):
        im = cv2.imread(data)
        im = self.square_image(im)
        if off:
            im = self.adjust(im, alpha=0.6, beta=0.0)
            im = cv2.rectangle(im, (2, 2), (im.shape[1]-2, im.shape[0]-2), (255, 255, 0), 10)

        # 上下反転
        buf = cv2.flip(im, 0)
        image_texture = Texture.create(size=(im.shape[1], im.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        return image_texture

    # 画像を正方形にする
    def square_image(self, img):
        h, w = img.shape[:2]
        if h > w:
            x = int((h-w)/2)
            img = img[x:x + w, :, :]
        elif h < w:
            x = int((w - h) / 2)
            img = img[:, x:x + h, :]

        return img

    # 画像の色を暗くする
    def adjust(self, img, alpha=1.0, beta=0.0):
        # 積和演算を行う。
        dst = alpha * img + beta
        # [0, 255] でクリップし、uint8 型にする。
        return np.clip(dst, 0, 255).astype(np.uint8)


class Screen_Two(Screen):
    def __init__(self, **kwargs):
        super(Screen_Two, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        button = Button(text="Go back to Screen One", size_hint=(1, None), height=100,pos_hint={'top': 1},on_release=self.switch_to_screen_one)

        # 読み込むディレクトリ
        image_dir = "./img/"


        # 画像ファイルの名前を管理
        self.image_name = ""
        #回数かくにん
        self.num_add=0
        self.hozon_im=""

        #mask
        self.haikei=""
        self.former=""
        self.masuku=""
        # 画像を表示するウィジェットの準備
        self.image = Image(size_hint=(1, 1))
        self.add_widget(self.image)

        # 画像ボタンを配置する、スクロールビューの定義
        sc_view = ScrollView(size_hint=(1, None), size=(self.width, self.height*4))

        # スクロールビューには１つのウィジェットしか配置できないため
        box = GridLayout(cols=5, spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        # 画像ボタンの一括定義、グリッドレイアウトに配置
        box = self.image_load(image_dir, box)

        sc_view.add_widget(box)



        self.add_widget(sc_view)
        layout.add_widget(button)
        self.add_widget(layout)

    # 画像ボタンの読み込み
    def image_load(self, im_dir, grid):
        images = sorted(os.listdir(im_dir))
        for image in images:
            button = MyButton(size_hint_y=None,
                              height=300,
                              source=os.path.join(im_dir, image),
                              group="g1")
            button.bind(on_press=self.set_image)
            grid.add_widget(button)

        return grid
    # 画像をボタンを押した時、画像ウィジェットに画像を表示
    def set_image(self, btn):
        if btn.state=="down":
            self.num_add+=1
            #self.image_name = btn.source
            #save_variable_content(str(self.num_add), 'output.txt')
            name_change=str(self.num_add)
            img=cv2.imread(btn.source)
            self.hozon_im= name_change+"output.jpg"
            #formerに画像があるならマスク画像を作成
            if os.path.exists(self.former):
                pokemon=self.former
                self.haikei=self.hozon_im
                cv2.imwrite(self.haikei,img)
                self.masuku="res"+self.haikei
                img=pikapika.masuku(pokemon,self.haikei)
                cv2.imwrite(self.masuku,img)
                self.image_name=self.masuku
            else:
                cv2.imwrite(self.hozon_im,img)
                self.former=self.hozon_im
                self.image_name=self.hozon_im
            #画面を更新
            Clock.schedule_once(self.update)
            #riset
            if os.path.exists(self.haikei):
                os.remove(pokemon)
                os.remove(self.haikei)
                self.former=""
            elif os.path.exists(self.masuku):
                os.remove(self.masuku)

    # 画面更新
    def update(self, t):
        self.image.source = self.image_name

    def switch_to_screen_one(self, *args):
        app = App.get_running_app()
        app.root.current = 'screen_one'




class Screen_Three(Screen):
    def __init__(self, **kwargs):
        super(Screen_Three, self).__init__(**kwargs)
        # 読み込むディレクトリ
        image_dir = "./img/"

        # 縦配置
        self.orientation = 'vertical'

        # 画像ファイルの名前を管理
        self.image_name = ""
        #回数かくにん
        self.num_add=0
        self.hozon_im=""

        # 画像を表示するウィジェットの準備
        self.image = Image(size_hint=(1, 1))
        self.add_widget(self.image)

        # 画像ボタンを配置する、スクロールビューの定義
        sc_view = ScrollView(size_hint=(1, None), size=(self.width, self.height*4))

        # スクロールビューには１つのウィジェットしか配置できないため
        box = GridLayout(cols=5, spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        # 画像ボタンの一括定義、グリッドレイアウトに配置
        box = self.image_load(image_dir, box)

        sc_view.add_widget(box)
        self.add_widget(sc_view)

        layout = BoxLayout(orientation='vertical')
        button = Button(text="Go back to Screen One", size_hint=(1, None), height=100,pos_hint={'top': 1},on_release=self.switch_to_screen_one)
        layout.add_widget(button)
        self.add_widget(layout)

    # 画像ボタンの読み込み
    def image_load(self, im_dir, grid):
        images = sorted(os.listdir(im_dir))
        for image in images:
            button = MyButton(size_hint_y=None,
                              height=300,
                              source=os.path.join(im_dir, image),
                              group="g1")
            button.bind(on_press=self.set_image)
            grid.add_widget(button)

        return grid

    # 画像をボタンを押した時、画像ウィジェットに画像を表示
    def set_image(self, btn):
        if btn.state=="down":
            self.num_add+=1
            #self.image_name = btn.source
            #save_variable_content(str(self.num_add), 'output.txt')
            name_change=str(self.num_add)
            img=cv2.imread(btn.source)
            img=emo.main(img)
            former=self.hozon_im
            self.hozon_im= name_change+"output.jpg"
            cv2.imwrite(self.hozon_im,img)
            self.image_name=self.hozon_im
            #画面を更新
            Clock.schedule_once(self.update)
            #前の画像消去
            if os.path.exists(former):
                os.remove(former)
            else:
                pass

    # 画面更新
    def update(self, t):
        self.image.source = self.image_name

    def switch_to_screen_one(self, *args):
        app = App.get_running_app()
        app.root.current = 'screen_one'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen_One(name='screen_one'))
        sm.add_widget(Screen_Two(name='screen_two'))
        sm.add_widget(Screen_Three(name='screen_three'))
        return sm


if __name__ == '__main__':
    MyApp().run()

