# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, OptionProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

from ttgo import ttgo_dir

class GoGame(BoxLayout):
    app = ObjectProperty(None)
    board = ObjectProperty(None)
    points = NumericProperty(None)
    pads = ObjectProperty(None)
    dead_stones = ListProperty([])
    current_player = OptionProperty("black", options=["black","white"])

    def __init__(self, **kwargs):
        super(GoGame, self).__init__(**kwargs)
        self.pads["black"].activate()

    def pad(self,color):
        return self.pads[color]

    def opponent_pad(self,color):
        return self.pads['white' if color == 'black' else 'black']

    def on_play(self,i,j,board):
        if self.handicap_adder:
            self.handicap_adder.parent.remove_widget(self.handicap_adder)
            self.handicap_adder = False
        last = self.current_player
        next = 'white' if last == 'black' else 'black'

        stones = board.adjacent_stones(i,j, color=next)
        groups = [ board.get_group(*pt) for pt in stones ]
        liberties = [ board.group_liberties(grp) for grp in groups ]

        # Atari notice
        self.pads[last].atari = False
        if [ lib for lib in liberties if 1 == len(lib) ]:
            self.pads[next].atari = True

        # Dim dead groups
        for idx in [ a for a in xrange(len(liberties)) if 0 == len(liberties[a]) ]:
            self.dead_stones.extend(groups[idx])
            for pt in groups[idx]:
                board[pt].dim()

        self.current_player = next
        self.pads[next].activate()
        self.pads[last].deactivate()


Factory.register("GoGame", GoGame)
Builder.load_file(ttgo_dir("gogame.kv"), rulesonly=True)
