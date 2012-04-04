# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
__version__ = '0.0010'   # Created: 2012-03-25

import logging
import re
import glob
import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window, Keyboard
from kivy.factory import Factory
from kivy.graphics import Rectangle, Line, Color, Ellipse
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty, OptionProperty, AliasProperty
from kivy.resources import resource_find
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget


class NumChooser(BoxLayout):
    app = ObjectProperty(None)
Factory.register("NumChooser", NumChooser)

class PlayerPad(Scatter):
    label = ObjectProperty(None)
    player = StringProperty("")

    def activate(self):
        self.label.bold = True
        self.label.color = [1,1,.25,1]
    def deactivate(self):
        self.label.bold = False
        self.label.color = [1,1,1,1]

Factory.register("PlayerPad", PlayerPad)

class GoStone(Widget):
    stone_color = StringProperty(None)
    annotation = StringProperty("")

    def boom(self,cb=None,*args):
        duration = .25
        frames = 30

        if hasattr(self, 'frame') and self.frame:
            self.frame += 1
            if self.frame <= frames:
                self.smoke.source = "smoke/smoke_%02d.png" % self.frame
                Clock.schedule_once(self.boom,duration/frames)
            else:
                self.frame = None
                if self.cb: self.cb()
        else:
            self.frame = 1
            self.smoke = Image(source="smoke/smoke_01.png",size=[2*x for x in self.size])# mipmap=True,
            self.smoke.center = self.center
            Animation(size=(0,0), center=self.center, d=duration).start(self)
            Animation(color=[0,0,0,0], d=duration).start(self.label)# also clear out 1px label remnant
            self.add_widget(self.smoke)
            self.cb = cb
            Clock.schedule_once(self.boom,duration/frames)

Factory.register("GoStone", GoStone)

class NewGame(AnchorLayout):
    app = ObjectProperty(None)
Factory.register("NewGame", NewGame)



class GoGame(BoxLayout):
    app = ObjectProperty(None)
    board = ObjectProperty(None)
    points = NumericProperty(None)
    pads = ObjectProperty(None)
    current_player = OptionProperty("black", options=["black","white"])

    def __init__(self, **kwargs):
        super(GoGame, self).__init__(**kwargs)
        self.pads[0].activate()

    def on_play(self,i,j):
        if self.current_player == 'black':
            self.current_player = 'white'
            self.pads[0].deactivate()
            self.pads[1].activate()
        else:
            self.current_player = 'black'
            self.pads[0].activate()
            self.pads[1].deactivate()

Factory.register("GoGame", GoGame)


class GoBoard(Widget):
    game       = ObjectProperty(None)
    turn       = NumericProperty(1)

    board_pad  = NumericProperty(10)
    points     = NumericProperty(None)
    box_size   = NumericProperty(None)

    def __init__(self, **kwargs):
        super(GoBoard, self).__init__(**kwargs)
        self.touch  = {}
        self.stones = []
        self.bind(points=self.build)
        self.bind(size=self.rescale, board_pad=self.rescale)

    def build(self, obj, n):
        self.canvas.clear()
        with self.canvas:
            self.image  = Rectangle( source="board.png", size=(100,100) )
            Color(0,0,0)
            self.hlines = [ Line(points=(0,0,1,1)) for i in xrange(self.points) ]
            self.vlines = [ Line(points=(0,0,1,1)) for i in xrange(self.points) ]
        self.board = [ [ None for i in xrange(self.points) ] for j in xrange(self.points) ]
        self.rescale(self, self.size)

    def rescale(self, obj, size):
        s = min(*self.size)

        # Board image
        self.image.size = (s,s)
        self.image.pos  = (x - int(s/2) for x in self.center)

        # Calculations
        self.grid_pos   = (self.image.pos[0] + self.board_pad, self.image.pos[1] + self.board_pad)
        self.box_size   = int( ( s - 2 * self.board_pad ) / self.points )

        # Stone images
        for i in xrange(self.points):
            for j in xrange(self.points):
                if self.board[i][j]:
                    self.board[i][j].size   = (self.box_size, self.box_size)
                    self.board[i][j].center = self.address2xy(i, j)

        # Lines
        (x_min,y_min) = self.address2xy(0,0)
        (x_max,y_max) = self.address2xy(self.points-1,self.points-1)

        for i in xrange(self.points):
            (x,y) = self.address2xy( i, i )
            self.hlines[i].points = [x_min,y,x_max,y]
            self.vlines[i].points = [x,y_min,x,y_max]

        self.canvas.ask_update()


    def _clip_to(self, a, low, high):
        if a < low:
            return low
        if a > high:
            return high
        return a

    def find_address(self, x, y):
        i = self._clip_to( int(( x - self.grid_pos[0] ) / self.box_size), 0, self.points - 1 )
        j = self._clip_to( int(( y - self.grid_pos[1] ) / self.box_size), 0, self.points - 1 )
        return (i,j)

    def address2xy(self, i, j):
        x = int( self.grid_pos[0] + i * self.box_size + self.box_size / 2 )
        y = int( self.grid_pos[1] + j * self.box_size + self.box_size / 2 )
        return (x,y)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):

            touch.grab(self)
            tpos = self.to_local(*touch.pos)
            (i, j) = self.find_address( *tpos )

            if self.board[i][j]:
                return
            else:
                self.touch[touch.uid] = GoStone(size=(self.box_size,self.box_size), stone_color=self.game.current_player)
                self.touch[touch.uid].center = self.address2xy(i,j)
                self.touch[touch.uid].annotation = str(self.turn)
                self.add_widget( self.touch[touch.uid] )

            return True

    def on_touch_move(self,touch):
        if touch.grab_current is self and self.touch.get(touch.uid, None):
            self.touch[touch.uid].center = self.to_local(*touch.pos)
            return True

    def on_touch_up(self,touch):
        if touch.grab_current is self and self.touch.get(touch.uid, None):
            (i, j) = self.find_address(*self.to_local(*touch.pos))
            stone = self.touch[touch.uid]
            del self.touch[touch.uid]
            if self.board[i][j]:
                stone.boom(cb=lambda: self.remove_widget(stone))
            else:
                self.board[i][j] = stone
                self.turn += 1
                self.game.on_play(i, j)
                ani = Animation( d=.1, t='in_out_sine', center=self.address2xy(i,j) )
                ani.start( stone )
            return True

Factory.register("GoBoard", GoBoard)


class TTGoApp(App):
    title = "TTGo"
    icon = 'themes/default/black.png'

    def build(self):
        kivy.resources.resource_add_path("glyphicons")
        kivy.resources.resource_add_path("themes/" + self.config.get('ttgo', 'theme'))
        for kv in glob.glob('ttgo/*.kv'):
            if kv != 'ttgo/ttgo.kv': Builder.load_file(kv, rulesonly=True)
        self.goto_screen("new")

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
        self.goto_screen("game", size=size)

    def goto_screen(self, screen_name, **opt):
        self.root.clear_widgets()
        if   screen_name == "new":
            widget = NewGame( app=self, size=self.root.size )
        elif screen_name == "game":
            widget = GoGame(app=self, points=opt['size'], size=self.root.size)
        self.root.add_widget( widget )
        self.screen = screen_name

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

if __name__ == '__main__':
    TTGoApp().run()
