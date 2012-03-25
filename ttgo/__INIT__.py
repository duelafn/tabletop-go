# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
import logging
import re
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.logger import Logger
from kivy.core.image import Image
from kivy.config import Config
from kivy.properties import NumericProperty, StringProperty
from kivy.graphics import Rectangle, Line, Color, Ellipse
from kivy.resources import resource_find

from PIL import Image


class GoGame(Widget):
    def __init__(self, **kwargs):
        super(GoGame, self).__init__(**kwargs)
        s = min( Config.getint('graphics', 'width'), Config.getint('graphics', 'height') ) - 50
        self.board = GoBoard( stones=19, pos=(25,25), size=(s,s) )
        self.add_widget( self.board )


# 9x9, 13x13, 17x17, or 19x19
class GoBoard(Scatter):
    stones = NumericProperty(0)
    padding = NumericProperty(10)

    def __init__(self, **kwargs):
        kwargs['do_rotation'] = False
        kwargs['do_scale'] = False
        kwargs['do_translation'] = False
        super(GoBoard, self).__init__(**kwargs)

        self._boxwidth  = int( (self.width  - 2 * self.padding) / self.stones )
        self._boxheight = int( (self.height - 2 * self.padding) / self.stones )
        top  = int( ( self.height - self.stones * self._boxheight ) / 2 )
        left = int( ( self.width  - self.stones * self._boxwidth  ) / 2 )
        bottom = self.height - self.stones * self._boxheight - top
        right  = self.width  - self.stones * self._boxwidth  - left
        self._padding = { 'top': top, 'right': right, 'bottom': bottom, 'left': left }
        self._px = px = { 'top': self.height-top, 'right': self.width-right, 'bottom': bottom, 'left': left }

        self.board = [ [ None for i in range(self.stones) ] for j in range(self.stones) ]
        with self.canvas:
            Rectangle(source=resource_find("board.png"), size=self.size)
            Color(0,0,0)
            x_min = left + int( self._boxwidth / 2 )
            x_max = x_min + self._boxwidth * (self.stones - 1)
            y_min = bottom + int( self._boxheight / 2 )
            y_max = y_min + self._boxheight * (self.stones - 1)
            for x in range(x_min, x_max+1, self._boxwidth):
                Line( points=( x,y_min, x,y_max ) )
            for y in range(y_min, y_max+1, self._boxheight):
                Line( points=( x_min,y, x_max,y ) )


class GoStone(Widget):
    turn_number = NumericProperty(0)
#    turn_number.bind( update_turn )

    color = StringProperty(None)
#    color.bind( update_source )

    def update_source(self):
        with self.canvas:
            Rectangle(source=self.color + '.png', pos=self.pos, size=self.size)

    # display turn number on top of stone
    def update_turn(self):
        if Config.getboolean( "ttgo", "show_turns" ):
            self.annotate(turn_number)

    def annotate(self, text):
        pass



class TTGoApp(App):
    title = "TTGo"
    icon = 'themes/default/black.png'

    def build(self):
        # Just add another path for the theme
        kivy.resources.resource_add_path("/home/duelafn/Surface/tabletop-go/themes/" + self.config.get('ttgo', 'theme'))
        self.game = GoGame()
        return self.game


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
