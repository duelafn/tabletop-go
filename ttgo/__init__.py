# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
__version__ = "0.2.0-dev"


import os.path

ttgo_parent_dir = (os.path.split(__file__))[0]
def ttgo_dir(path=None):
    if path is None:
        return os.path.join(ttgo_parent_dir)
    else:
        return os.path.join(ttgo_parent_dir, path)


import glob
import kivy

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.logger import Logger


from ttgo.gogame import GoGame
from ttgo.kvwidgets import NewGame

import ttgo.goboard
import ttgo.gostone
import ttgo.playerpad


class TTGoApp(App):
    title = "TTGo"
    icon = ttgo_dir('data/ttgo.png')

    def build(self):
        kivy.resources.resource_add_path(ttgo_dir("data/glyphicons"))
        kivy.resources.resource_add_path(ttgo_dir("data/themes/" + self.config.get('ttgo', 'theme')))
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
