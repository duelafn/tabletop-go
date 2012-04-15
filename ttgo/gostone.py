# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from ttgo import ttgo_dir


class GoStone(Widget):
    stone_color = StringProperty(None)
    annotation = StringProperty("")
    default_anim_duration = .25

    def _alpha(self,alpha,duration=default_anim_duration,shadow=0):
        Animation(color=[1,1,1,alpha]).start(self.image)
        Animation(color=self.label.color[0:3]+[alpha]).start(self.label)
        Animation(color=[1,0,0,shadow]).start(self.shadow)

    def normal(self,duration=default_anim_duration):
        self._alpha(1, duration)

    def dim(self,duration=default_anim_duration,alpha=.4):
        self._alpha(alpha, duration)

    def highlight(self,duration=default_anim_duration):
        self._alpha(1, duration, shadow=1)

    def blink(self,c=2):
        duration = .75
        count = [c]

        def run_anim(dt):
            if count[0] > 0:
                count[0] -= 1
                Clock.schedule_once(lambda dt: self._alpha(0,duration/2))
                Clock.schedule_once(lambda dt: self._alpha(1,duration/2), duration/2)
                Clock.schedule_once(run_anim, duration)

        Clock.schedule_once(run_anim)


    def boom(self,cb=None,*args):
        duration = .25
        frames = 30

        # Note: we do not use self.frame = 0
        if getattr(self, "frame", None):
            self.frame += 1
            if self.frame <= frames:
                self.smoke.source = "smoke/smoke_%02d.png" % self.frame
                Clock.schedule_once(self.boom,duration/frames)
            else:
                self.frame = None
                if self.cb: self.cb()
        else:
            self.frame = 1
            self.smoke = Image(source="smoke/smoke_01.png",size=[2*x for x in self.size])# mipmap=True,
            self.smoke.center = self.center
            Animation(size=(0,0), center=self.center, d=duration).start(self)
            Animation(color=[0,0,0,0], d=duration).start(self.label)# also clear out 1px label remnant
            self.add_widget(self.smoke)
            self.cb = cb
            Clock.schedule_once(self.boom,duration/frames)

Factory.register("GoStone", GoStone)
Builder.load_file(ttgo_dir("gostone.kv"), rulesonly=True)
