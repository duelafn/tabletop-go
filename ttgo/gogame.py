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
        self.pads["black"].activate()

    def on_play(self,i,j):
        last = self.current_player
        next = 'white' if last == 'black' else 'black'

        self.current_player = next
        self.pads[next].activate()
        self.pads[last].deactivate()

Factory.register("GoGame", GoGame)
