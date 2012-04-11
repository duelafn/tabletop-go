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
        if not (0 <= i < self.points and 0 <= j < self.points):
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


    def adjacent_indices(self, i, j):
        """Set of valid adjacent indices

        returns set([ (i-1,j), (i+1,j), (i,j-1), (i,j+1) ]) but excludes
        invalid (off the board) indices.
        """
        if not (0 <= i < self.points and 0 <= j < self.points):
            raise IndexError("(%d,%d) Out of bounds" % (i,j))

        ind = set();
        if i > 0:                ind.add((i-1,j))
        if j > 0:                ind.add((i,j-1))
        if i < self.points - 1:  ind.add((i+1,j))
        if j < self.points - 1:  ind.add((i,j+1))
        return ind


    def adjacent_stones(self, i, j, color=None):
        """Set of adjacent indices containing stones.

        Keyword Args:

        * color=None - if set, only indices containing stones of the given
          color will be returned.
        """
        ind = set()
        for pt in [ (i-1,j), (i+1,j), (i,j-1), (i,j+1) ]:
            stone = self.get(*pt)
            if stone and ( not(color) or color == stone.stone_color ):
                ind.add(pt)
        return ind


    def adjacent_points(self, i, j):
        """Set of adjacent indices without stones."""
        ind = set()
        for pt in self.adjacent_indices(i,j):
            if not(self[pt]):
                ind.add(pt)
        return ind


    def get_group(self, i, j):
        """go.get_group(i,j) → set of indices

        Returns empty set if no stone at (i,j). Else, returns set of
        indices that are part of the same connected group as the stone at
        (i,j).
        """
        if not(self[i,j]):
            return set()

        group = set([(i,j)])
        self.grow_group(group)
        return group

    def grow_group(self, group):
        """go.grow_group(group)

        Modify the given set of indices by adding adjacent indices of the
        same color. Bad things can happen if the given group has mixed
        colors or contains points without a stone.
        """
        if not(group):
            return

        untested = group.copy()
        seen     = group.copy()
        x = untested.pop()
        color = self[x].stone_color
        untested.add(x)

        while untested:
            (i,j) = untested.pop()
            for pt in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                if not(pt in seen):
                    seen.add(pt)
                    try:
                        stone = self[pt]
                        if stone and stone.stone_color == color:
                            group.add(pt)
                            untested.add(pt)
                    except IndexError, err:
                        pass

    def group_liberties(self, group):
        """go.group_liberties(group) → set of empty points adjacent to the group

        Note: Counts only empty points - does not consider the color of the
        stones in adjacent slots. Furthermore, strange things might happen
        if any of the group indices do not have stones.
        """
        libs = set()

        for (i,j) in group:
            for pt in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                try:
                    if not(self[pt]):
                        libs.add(pt)
                except IndexError, err:
                    pass

        return libs
