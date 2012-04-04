# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.scatter import Scatter


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
