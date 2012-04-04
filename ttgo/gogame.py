# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, OptionProperty
from kivy.uix.boxlayout import BoxLayout


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