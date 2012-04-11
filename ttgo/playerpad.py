# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter

from ttlib.click import DblTap


class PlayerPad(Scatter):
    label = ObjectProperty(None)
    player = StringProperty("")
    captures = NumericProperty(0)
    atari = BooleanProperty(False)

    def activate(self):
        self.label.bold = True
        self.label.color = [1,1,.25,1]
    def deactivate(self):
        self.label.bold = False
        self.label.color = [1,1,1,1]

Factory.register("PlayerPad", PlayerPad)

class NameBanner(DblTap,Button):

    def on_dbl_click(self):
        # pop out keyboard and allow changing name
        pass
Factory.register("NameBanner", NameBanner)
