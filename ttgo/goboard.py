# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.animation import Animation
from kivy.factory import Factory
from kivy.graphics import Rectangle, Line, Color, Ellipse
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

from go.goobject import GoObject
from ttgo.gostone import GoStone


class GoBoard(Widget):
    game       = ObjectProperty(None)
    turn       = NumericProperty(1)

    board_pad  = NumericProperty(10)
    points     = NumericProperty(None)
    box_size   = NumericProperty(None)

    def __init__(self, **kwargs):
        super(GoBoard, self).__init__(**kwargs)
        self.touch  = {}
        self.board  = GoObject(points=self.points)
        self.stones = []
        self.bind(points=self.build)
        self.bind(size=self.rescale, board_pad=self.rescale)

    def build(self, obj, n):
        self.board.points = self.points
        self.canvas.clear()
        with self.canvas:
            self.image  = Rectangle( source="board.png", size=(100,100) )
            Color(0,0,0)
            self.hlines = [ Line(points=(0,0,1,1)) for i in xrange(self.points) ]
            self.vlines = [ Line(points=(0,0,1,1)) for i in xrange(self.points) ]
        self.rescale(self, self.size)

    def rescale(self, obj, size):
        s = min(*self.size)

        # Board image
        self.image.size = (s,s)
        self.image.pos  = (x - int(s/2) for x in self.center)

        # Calculations
        self.grid_pos   = (self.image.pos[0] + self.board_pad, self.image.pos[1] + self.board_pad)
        self.box_size   = int( ( s - 2 * self.board_pad ) / self.points )

        # Stone images
        for i in xrange(self.points):
            for j in xrange(self.points):
                stone = self.board[i,j]
                if stone:
                    stone.size   = (self.box_size, self.box_size)
                    stone.center = self.address2xy(i, j)

        # Lines
        (x_min,y_min) = self.address2xy(0,0)
        (x_max,y_max) = self.address2xy(self.points-1,self.points-1)

        for i in xrange(self.points):
            (x,y) = self.address2xy( i, i )
            self.hlines[i].points = [x_min,y,x_max,y]
            self.vlines[i].points = [x,y_min,x,y_max]

        self.canvas.ask_update()


    def _clip_to(self, a, low, high):
        if a < low:
            return low
        if a > high:
            return high
        return a

    def find_address(self, x, y):
        i = self._clip_to( int(( x - self.grid_pos[0] ) / self.box_size), 0, self.points - 1 )
        j = self._clip_to( int(( y - self.grid_pos[1] ) / self.box_size), 0, self.points - 1 )
        return (i,j)

    def address2xy(self, i, j):
        x = int( self.grid_pos[0] + i * self.box_size + self.box_size / 2 )
        y = int( self.grid_pos[1] + j * self.box_size + self.box_size / 2 )
        return (x,y)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):

            touch.grab(self)
            tpos = self.to_local(*touch.pos)
            (i, j) = self.find_address( *tpos )

            if self.board[i,j]:
                return
            else:
                self.touch[touch.uid] = GoStone(size=(self.box_size,self.box_size), stone_color=self.game.current_player)
                self.touch[touch.uid].center = self.address2xy(i,j)
                self.touch[touch.uid].annotation = str(self.turn)
                self.add_widget( self.touch[touch.uid] )

            return True

    def on_touch_move(self,touch):
        if touch.grab_current is self and self.touch.get(touch.uid, None):
            self.touch[touch.uid].center = self.to_local(*touch.pos)
            return True

    def on_touch_up(self,touch):
        if touch.grab_current is self and self.touch.get(touch.uid, None):
            (i, j) = self.find_address(*self.to_local(*touch.pos))
            stone = self.touch[touch.uid]
            del self.touch[touch.uid]
            if self.board[i,j]:
                stone.boom(cb=lambda: self.remove_widget(stone))
            else:
                self.board[i,j] = stone
                self.turn += 1
                self.game.on_play(i, j, self.board)
                ani = Animation( d=.1, t='in_out_sine', center=self.address2xy(i,j) )
                ani.start( stone )
            return True

Factory.register("GoBoard", GoBoard)
