# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
__version__ = "0.2.0-dev"


import os.path

ttgo_parent_dir = (os.path.split(__file__))[0]
def ttgo_dir(*path):
    return os.path.join(ttgo_parent_dir, *path)


import glob
import kivy

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.logger import Logger

from ttlib.ttapp import TTApp

from ttgo.gogame import GoGame
from ttgo.kvwidgets import NewGame

import ttgo.goboard
import ttgo.gostone
import ttgo.playerpad


class TTGoApp(TTApp):
    title = "TTGo"
    icon = ttgo_dir('data/ttgo.png')

    def data_dir(self, *args):
        return os.path.join(ttgo_parent_dir, 'data', *args)

    def __init__(self, *arg, **kwargs):
        self.app_name = 'ttgo'
        super(TTGoApp,self).__init__(*arg, **kwargs)

    def start_game(self, size):
        try:
            size = int(size)
        except ValueError, e:
            return
        self.goto_screen("game", size=size)

    def goto_screen(self, screen_name, **opt):
        super(TTGoApp,self).goto_screen(screen_name, **opt)

        if   screen_name == "new":
            widget = NewGame( app=self )
        elif screen_name == "game":
            widget = GoGame(app=self, points=opt['size'])
        self.root.add_widget( widget )
        self.screen = screen_name

    def build_config(self, config):
        config.setdefaults('ttgo', {
            'theme': 'default'
        })

    def on_config_change(self, config, section, key, value):
        super(TTGoApp,self).on_config_change(config, section, key, value)
        if config is self.config:
            if self.screen == 'game' and (section, key) == (self.app_name, 'theme'):
                self.root.children[0].board.reload_theme()

    def build_settings(self, settings):
        jsondata = """
[
    { "type": "options",
      "title": "Theme",
      "desc": "Board and go piece theme",
      "section": "ttgo",
      "key": "theme",
      "options": ["default", "fire+ice"]
    }
]
"""
        settings.add_json_panel('TTGo', self.config, data=jsondata)
