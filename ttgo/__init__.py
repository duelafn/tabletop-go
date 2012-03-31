# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
__version__ = '0.0005'   # Created: 2012-03-25

import logging
import re
import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window, Keyboard
from kivy.factory import Factory
from kivy.graphics import Rectangle, Line, Color, Ellipse
from kivy.logger import Logger
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.resources import resource_find
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget


class NumChooser(BoxLayout):
    app = ObjectProperty(None)

class GoStone(Widget):
    color = StringProperty(None)
    annotation = StringProperty("")

class NewGame(AnchorLayout):
    app = ObjectProperty(None)



class GoGame(AnchorLayout):
    stones  = NumericProperty(0)
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GoGame, self).__init__(**kwargs)
        self.player = 'black'
        s = min( Config.getint('graphics', 'width'), Config.getint('graphics', 'height') ) - 50
        self.board = GoBoard( stones=self.stones, size=(s,s), game=self )
        self.add_widget( self.board )

    def on_play(self,i,j):
        if self.player == 'black':
            self.player = 'white'
        else:
            self.player = 'black'


# 9x9, 13x13, 17x17, or 19x19
class GoBoard(Scatter):
    stones  = NumericProperty(0)
    padding = NumericProperty(10)
    turn    = NumericProperty(1)

    def __init__(self, **kwargs):
        super(GoBoard, self).__init__(**kwargs)
        self.touch = {}
        self.game  = kwargs['game']

        self._boxwidth  = int( (self.width  - 2 * self.padding) / self.stones )
        self._boxheight = int( (self.height - 2 * self.padding) / self.stones )
        self.stone_size = min( self._boxwidth, self._boxheight )

        top  = int( ( self.height - self.stones * self._boxheight ) / 2 )
        left = int( ( self.width  - self.stones * self._boxwidth  ) / 2 )
        bottom = self.height - self.stones * self._boxheight - top
        right  = self.width  - self.stones * self._boxwidth  - left
        self._padding = { 'top': top, 'right': right, 'bottom': bottom, 'left': left }
        self._px = px = { 'top': self.height-top, 'right': self.width-right, 'bottom': bottom, 'left': left }

        self.board = [ [ None for i in xrange(self.stones) ] for j in xrange(self.stones) ]
        with self.canvas:
            Rectangle(source="board.png", size=self.size)
            Color(0,0,0)
            x_min = left + int( self._boxwidth / 2 )
            x_max = x_min + self._boxwidth * (self.stones - 1)
            y_min = bottom + int( self._boxheight / 2 )
            y_max = y_min + self._boxheight * (self.stones - 1)
            for x in xrange(x_min, x_max+1, self._boxwidth):
                Line( points=( x,y_min, x,y_max ) )
            for y in xrange(y_min, y_max+1, self._boxheight):
                Line( points=( x_min,y, x_max,y ) )

    def _clip_to(self, a, low, high):
        if a < low:
            return low
        if a > high:
            return high
        return a

    def find_address(self, x, y):
        i = self._clip_to( int(( x - self._px['left'] )   / self._boxwidth),   0, self.stones - 1 )
        j = self._clip_to( int(( y - self._px['bottom'] ) / self._boxheight),  0, self.stones - 1 )
        return (i,j)

    def address2xy(self, i, j):
        x = int( self._px['left']   + i * self._boxwidth  + ( self._boxwidth  - self.stone_size ) / 2 )
        y = int( self._px['bottom'] + j * self._boxheight + ( self._boxheight - self.stone_size ) / 2 )
        return (x,y)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
#            super(GoBoard, self).on_touch_down(touch)# while testing transforsm
#            if touch.is_double_tap:
#                # TODO: "select" group (alpha=.5), determine if it is captured, and capture (or show a Bubble)
#                pass

            touch.grab(self)
            tpos = self.to_local(*touch.pos)
            (i, j) = self.find_address( *tpos )

            if self.board[i][j]:
                self.touch[touch.uid] = self.board[i][j]
                self.board[i][j] = None
            else:
                self.touch[touch.uid] = GoStone(width=self.stone_size, height=self.stone_size, color=self.game.player)
                self.touch[touch.uid].center = tpos
                self.touch[touch.uid].annotation = str(self.turn)
                self.turn = self.turn + 1
                self.add_widget( self.touch[touch.uid] )

            return True

    def on_touch_move(self,touch):
        if touch.grab_current is self and self.touch.get(touch.uid, None):
#            super(GoBoard, self).on_touch_move(touch)# while testing transforsm
            self.touch[touch.uid].center = self.to_local(*touch.pos)
            return True

    def on_touch_up(self,touch):
        if touch.grab_current is self and self.touch.get(touch.uid, None):
#            super(GoBoard, self).on_touch_up(touch)# while testing transforsm
            # TODO: look for adjacent capture groups and either select or highlight (alpha=.5) group
            (i, j) = self.find_address(*self.to_local(*touch.pos))
            self.board[i][j] = self.touch[touch.uid]
            del self.touch[touch.uid]
            ani = Animation( d=.1, t='in_out_sine', pos=self.address2xy(i,j) )
            ani.start( self.board[i][j] )
            self.game.on_play(i, j)
            return True

class TTGoApp(App):
    title = "TTGo"
    icon = 'themes/default/black.png'

    def build(self):
        kivy.resources.resource_add_path("themes/" + self.config.get('ttgo', 'theme'))
        self.screens = { "new":  NewGame(app=self) }
        self.root = AnchorLayout()
        self.goto_screen("new")
        return self.root

    def on_start(self):
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, win, key, scancode, string, modifiers):
        if key == 292:
            win.toggle_fullscreen()
            win.update_viewport()
            return True
        elif key == 27:
            if self.screen == "new":
                exit()
            else:
                self.goto_screen("new")
            return True

    def start_game(self, size):
        try:
            size = int(size)
        except ValueError, e:
            return
        self.screens["game"] = GoGame(app=self, stones=size)
        self.goto_screen("game")

    def goto_screen(self, screen_name):
        self.root.clear_widgets()
        self.screen = screen_name
        self.root.add_widget(self.screens[screen_name])


    def build_config(self, config):
        config.setdefaults('ttgo', {
            'theme': 'default'
        })

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('ttgo', 'theme'):
                print( 'changed to theme:', value )

    def build_settings(self, settings):
        jsondata = """
[   { "type": "title",
      "title": "TTGo"
    },

    { "type": "options",
      "title": "Theme",
      "desc": "Board and go piece theme",
      "section": "ttgo",
      "key": "theme",
      "options": ["default", "missing_theme"]
    }
]
"""
        settings.add_json_panel('TTGo application', self.config, data=jsondata)

Factory.register("NumChooser", NumChooser)

if __name__ == '__main__':
    TTGoApp().run()
