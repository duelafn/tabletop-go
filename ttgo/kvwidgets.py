# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter

from ttgo import ttgo_dir


class NumChooser(BoxLayout):
    app = ObjectProperty(None)
Factory.register("NumChooser", NumChooser)

class NewGame(AnchorLayout):
    app = ObjectProperty(None)
Builder.load_file(ttgo_dir("newgame.kv"), rulesonly=True)
Factory.register("NewGame", NewGame)
