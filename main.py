import random

from kivy.app import App
from kivy.uix.widget import Widget
#from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

sfx_flap = SoundLoader.load('C:\Projekt\OiramRepus/smb_jump-small.wav')
sfx_score = SoundLoader.load('C:\Projekt\OiramRepus/smb_coin.wav')
sfx_die = SoundLoader.load('C:\Projekt\OiramRepus/smb_mariodie.wav')

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x = self.width)
        self.add_widget(self.image_dupe)
        
    def update(self):
        self.image.x -= 1
        self.image_dupe.x -= 1

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width

class Bird(Sprite):
    def __init__(self, pos):
        super(Bird, self).__init__(source='C:\Projekt\OiramRepus/crate.png', pos=pos)
        self.velocity_y = 0
        self.gravity = -.15

    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y

    def on_touch_down(self, *ignore):
        self.velocity_y = 4
        sfx_flap.play()

    def get_point(self):
        print('Point!')
        self.velocity_y = 3
        

##class Ground(Sprite):
##    def update(self):
##        self.x -= 2
##        if self.x < -2:
##            self.x += 2

class Ground(Widget):
    def __init__(self, source):
        super(Ground, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x = self.width)
        self.add_widget(self.image_dupe)
        
    def update(self):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width

class Pipe(Widget):
    def __init__(self, pos):
        super(Pipe, self).__init__(pos=pos)
        self.bottom_image = Sprite(source='C:\Projekt\OiramRepus/mario.png')
        self.bottom_image.pos = (self.x, self.y - self.bottom_image.height)
        self.add_widget(self.bottom_image)
        self.width = self.bottom_image.width
        self.scored = False

    def update(self):
        self.x -= 2
        self.bottom_image.x = self.x
        if self.right < 0:
            self.parent.remove_widget(self)

class Pipes(Widget):
    add_pipe = 0
    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_pipe -= dt
        if self.add_pipe < 0:
            y = 98
            self.add_widget(Pipe(pos=(self.width, y)))
            self.add_pipe = random.randrange(1, 3)

class Block1(Widget):
    def __init__(self, pos):
        super(Block1, self).__init__(pos=pos)
        self.block_image = Sprite(source='C:\Projekt\OiramRepus/block2.png')
        self.block_image.pos = (self.x, self.y - self.block_image.height)
        self.add_widget(self.block_image)
        self.width = self.block_image.width
        

    def update(self):
        self.x -= 2
        self.block_image.x = self.x
        if self.right < 0:
            self.parent.remove_widget(self)

class Blocks(Widget):
    add_block = 0
    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_block -= dt
        if self.add_block < 0:
            y = random.randrange(120, 300)
            self.add_widget(Block1(pos=(self.width, y)))
            self.add_block = random.randrange(1, 3)
    

class Game(Widget):

    def __init__(self):
        super(Game, self).__init__()
        self.background = Background(source='C:\Projekt\OiramRepus/background.png')
        self.size = self.background.size
        self.add_widget(self.background)
        self.ground = Ground(source='C:\Projekt\OiramRepus/ground.png')
        self.pipes = Pipes(pos=(0, self.ground.height), size=self.size)
        self.add_widget(self.pipes)
        self.blocks = Blocks(pos=(0, self.ground.height), size=self.size)
        self.add_widget(self.blocks)
        self.add_widget(self.ground)
        self.score_label = Label(center_x=self.center_x,
                                 top=self.top - 30, text='0')
        self.add_widget(self.score_label)
        self.over_label = Label(center=self.center, opacity=0,
                                text='Game Over!')
        self.add_widget(self.over_label)
        self.bird = Bird(pos=(20, self.height / 2))
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.game_over = False
        self.score = 0

    def update(self, dt):
        if self.game_over:
            return
        self.background.update()
        self.bird.update()
        self.ground.update()
        self.pipes.update(dt)
        self.blocks.update(dt)

        if self.bird.collide_widget(self.ground):
            self.game_over = True

        for pipe in self.pipes.children:
            if pipe.bottom_image.collide_widget(self.bird):
                self.bird.get_point()
                self.score += 1
                self.score_label.text = str(self.score)
                sfx_score.play()
                
        for block1 in self.blocks.children:
            if block1.block_image.collide_widget(self.bird):
                self.game_over = True
           
                
        
        if self.game_over:
            sfx_die.play()
            self.over_label.opacity = 1
            self.bind(on_touch_down=self._on_touch_down)
            

    def _on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Menu())

class Menu(Widget):
    def __init__(self):
        super(Menu, self).__init__()
        self.add_widget(Sprite(source='C:\Projekt\OiramRepus/background2.png'))
        self.size = self.children[0].size
        self.add_widget(Ground(source='C:\Projekt\OiramRepus/ground.png'))
        

    def on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Game())
            
        

class GameApp(App):
    def build(self):
        top = Widget()
        top.add_widget(Menu())
        Window.size = top.children[0].size
        return top

    
if __name__ == '__main__':
    GameApp().run()
