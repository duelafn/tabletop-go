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

    def on_play(self,i,j,board):
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
            for pt in groups[idx]:
                board[pt].dim()

        self.current_player = next
        self.pads[next].activate()
        self.pads[last].deactivate()


Factory.register("GoGame", GoGame)
