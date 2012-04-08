# -*- coding: utf-8 -*-
"""
GoObject - A go board object with basic analysis functions
"""

from __future__ import division, absolute_import, print_function

class GoObject(object):

    def __init__(self, points=19, **opt):
        """go = GoObject( points )

        points - the board "size", all boards are square with points × points stones
        """
        super(GoObject, self).__init__(**opt)
        self.board  = {}
        self.points = points

    def __len__(self):
        """len(go) → number of stones placed"""
        return len(self.board)

    def __getitem__(self, key):
        """go[i,j] → stone at index (i,j) or None

        raises IndexError unless 0 ≤ i,j < self.points
        """
        (i,j) = key
        if i < 0 or i >= self.points or j < 0 or j >= self.points:
            raise IndexError("(%d,%d) Out of bounds" % key)
        return self.board.get((i,j), None)

    def __setitem__(self, key, val):
        """go[i,j] = whatever

        raises IndexError unless 0 ≤ i,j < self.points
        raises LookupError if stone already exists at (i,j)

        "whatever" is expected to implement the GoStone interface. Namely,

            stone_color = StringProperty(None)
            annotation  = StringProperty("")
        """
        if self[key]:
            raise LookupError("May not overwrite stone at (%d, %d)" % key)
        self.board[key] = val

    def __delitem__(self, key):
        """del go[i,j]

        raises IndexError unless 0 ≤ i,j < self.points
        does nothing (raises no error) if i,j already empty
        """
        if self[key]:
            del self.board[key]

    def __iter__(self):
        """iter(go) → key (tuples: (i,j) with stones) iterator"""
        return iter(self.board)

    def __contains__(self, item):
        """(i,j) in go → boolesn"""
        return item in self.board


    def get(self, i, j, dflt=None):
        """go.get(i,j, dflt=None) → get index, allowing override of default"""
        return self.board.get((i,j), dflt)

    def get_group(self, i, j, groups=None, color=None):
        """go.get_group(i,j) → list of indices

        Keyword Args:

        color  - "black" or "white". Default: color of stone at (i,j)
        groups - dictionary {(a,b): True} of pre-computed group. Default: {}
        """
        groups = groups or {}

        # Stop if no stole at (i,j), or if we already visited this node
        if not(self[i,j]) or groups.get((i,j), None):
            return groups.keys()

        if not color:
            color = self[i,j].stone_color

        if not color == self[i,j].stone_color:
            return groups.keys()

        groups[(i,j)] = True

        for pt in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            try:
                self.get_group(*pt, groups=groups, color=color)
            except IndexError, err:
                pass

        return groups.keys()
