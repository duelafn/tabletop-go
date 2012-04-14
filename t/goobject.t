#!/usr/bin/python
import unittest2
import sys
sys.path.append("")

from gogame.goobject import GoObject


class White(object):
    def __init__(self, color="white", **opt):
        super(White, self).__init__(**opt)
        self.stone_color = color
class Black(object):
    def __init__(self, color="black", **opt):
        super(Black, self).__init__(**opt)
        self.stone_color = color


w = White()
b = Black()

boards = {
    "white_only": {(1,0):w,(1,1):w,(2,1):w,(2,2):w,(0,3):w,(1,3):w,(2,3):w,(3,3):w,(1,4):w,(2,4):w,(3,4):w,(1,5):w,(2,5):w,(3,5):w},
    "ll1": { (0,0):w, (1,0):b, (0,1):b },
    "ll3": { (0,0):w, (1,0):w, (0,1):w, (2,0):b, (1,1):b, (0,2):b },
    "T1":  { (1,1):w, (0,2):b, (1,2):b, (2,2):b, (0,3):w, (1,3):b, (1,4):w },
    }



class BasicAccess(unittest2.TestCase):
    def test_sequence_funcs(self):
        go = GoObject()
        go.board = boards["white_only"].copy()

        self.assertEqual( len(go), 14, "len" )

        self.assertEqual( go[2,3], w,  "Getter" )
        self.assertIsNone( go[0,0],  "Getter for non-existant" )
        self.assertRaises( IndexError, lambda x: go[19,19], "getter: IndexError when out of bounds" )

        go[0,0] = w
        def python_lambdas_suck_1(x):
            go[19,19] = w
        self.assertEqual( go[0,0], w,     "Setter" )
        self.assertRaises( IndexError, python_lambdas_suck_1, "setter: IndexError when out of bounds" )

        del go[2,3]
        self.assertIsNone( go[2,3],  "del" )
        def python_lambdas_suck_2(x):
            del go[19,19]
        self.assertRaises( IndexError, python_lambdas_suck_2, "del: IndexError when out of bounds" )

        self.assertIn(    (3,4),   go, "__contains__" )
        self.assertNotIn( (3,1),   go, "not __contains__" )
        self.assertNotIn( (19,19), go, "__contains__ out of bounds" )

        self.assertEqual( go.get(3,4, 42), w, "get() existing" )
        self.assertEqual( go.get(9,9, 42), 42, "get() non-existing" )
        self.assertEqual( go.get(19,19, 42), 42, "get() out of bounds" )

    def test_small_board(self):
        go = GoObject(points=5)
        go.board = boards["T1"].copy()

        self.assertEqual( len(go), 7, "len" )

        self.assertEqual( go[1,2], b,  "Getter" )
        self.assertIsNone( go[0,0],  "Getter for non-existant" )
        self.assertRaises( IndexError, lambda x: go[5,5], "getter: IndexError when out of bounds" )

        go[0,0] = w
        def python_lambdas_suck_1(x):
            go[5,5] = w
        self.assertEqual( go[0,0], w,     "Setter" )
        self.assertRaises( IndexError, python_lambdas_suck_1, "setter: IndexError when out of bounds" )

        del go[1,2]
        self.assertIsNone( go[1,2],  "del" )
        def python_lambdas_suck_2(x):
            del go[5,5]
        self.assertRaises( IndexError, python_lambdas_suck_2, "del: IndexError when out of bounds" )


class TestGrouping(unittest2.TestCase):
    """
python -mtimeit \
-s 'from gogame.goobject import GoObject' \
-s 'class S(object): pass' \
-s 'w = S()' \
-s 'w.stone_color = "white"' \
-s 'go = GoObject()' \
-s 'go.board = {(1,0):w,(1,1):w,(2,1):w,(2,2):w,(0,3):w,(1,3):w,(2,3):w,(3,3):w,(1,4):w,(2,4):w,(3,4):w,(1,5):w,(2,5):w,(3,5):w}'  \
'go.get_group(2,3)'
   """

    def test_get_group(self):
        go = GoObject()
        go.board = boards["white_only"].copy()
        the_group = boards["white_only"].keys()

        self.assertItemsEqual(go.get_group(2,3), the_group, 'get_group: big group from loc 1')
        self.assertItemsEqual(go.get_group(1,0), the_group, 'get_group: big group from loc 2')
        self.assertItemsEqual(go.get_group(0,0), [],        'get_group: empty location w/neighbor')
        self.assertItemsEqual(go.get_group(9,9), [],        'get_group: empty location no neighbors')

        go.board = boards["ll1"].copy()
        self.assertItemsEqual(go.get_group(0,0), [(0,0)], 'get_group: single item group')

        go.board = boards["ll3"].copy()
        self.assertItemsEqual(go.get_group(0,0), [(0,0),(1,0),(0,1)], 'get_group: corner group')

        go.board = boards["T1"].copy()
        self.assertItemsEqual(go.get_group(0,2), [(0,2),(1,2),(2,2),(1,3)], 'get_group: inverted T')


    def test_grow_group(self):
        go = GoObject()
        go.board = boards["white_only"].copy()
        the_group = boards["white_only"].keys()

        grown = set([(2,3)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, the_group, 'grow_group: big group from loc 1')

        grown = set([(2,3),(2,2)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, the_group, 'grow_group: big group from connected starter set')

        grown = set([(2,3),(3,5)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, the_group, 'grow_group: big group from disconnected starter set')

        grown = set([(1,0)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, the_group, 'grow_group: big group from loc 2')

        go.board = boards["ll1"].copy()
        grown = set([(0,0)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, [(0,0)], 'grow_group: single item group')

        go.board = boards["ll3"].copy()
        grown = set([(0,0)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, [(0,0),(1,0),(0,1)], 'grow_group: corner group')

        go.board = boards["T1"].copy()
        grown = set([(0,2)])
        go.grow_group(grown)
        self.assertItemsEqual(grown, [(0,2),(1,2),(2,2),(1,3)], 'grow_group: inverted T')



class TestLiberties(unittest2.TestCase):

    def test_group_liberties(self):
        go = GoObject()

        go.board = boards["ll1"].copy()
        self.assertItemsEqual(go.group_liberties(go.get_group(0,0)), [], 'group_liberties: dead item')

        go.board = boards["ll3"].copy()
        self.assertItemsEqual(go.group_liberties(go.get_group(0,0)), [], 'group_liberties: dead corner group')

        go.board = boards["T1"].copy()
        self.assertItemsEqual(go.group_liberties(go.get_group(0,2)), [(0,1),(2,1),(3,2),(2,3)], 'group_liberties: alive T')



class TestAdjacent(unittest2.TestCase):

    def test_adjacent_indices(self):
        go = GoObject()
        go.board = boards["T1"].copy()

        self.assertItemsEqual(go.adjacent_indices(0,0),   [(0,1),(1,0)], 'adjacent_indices: corner 1')
        self.assertItemsEqual(go.adjacent_indices(18,18), [(18,17),(17,18)], 'adjacent_indices: corner 2')
        self.assertItemsEqual(go.adjacent_indices(0,2),   [(0,3),(1,2),(0,1)], 'adjacent_indices: side')
        self.assertItemsEqual(go.adjacent_indices(5,6),   [(4,6),(6,6),(5,5),(5,7)], 'adjacent_indices: middle')

    def test_adjacent_stones(self):
        go = GoObject()
        go.board = boards["T1"].copy()

        self.assertItemsEqual(go.adjacent_stones(5,5),   [], 'adjacent_stones: nowhere')
        self.assertItemsEqual(go.adjacent_stones(18,18), [], 'adjacent_stones: empty corner')
        self.assertItemsEqual(go.adjacent_stones(0,1),   [(0,2),(1,1)], 'adjacent_stones: side')
        self.assertItemsEqual(go.adjacent_stones(2,3),   [(2,2),(1,3)], 'adjacent_stones: middle')

    def test_adjacent_points(self):
        go = GoObject()
        go.board = boards["T1"].copy()

        self.assertItemsEqual(go.adjacent_points(5,5),   [(4,5),(6,5),(5,4),(5,6)], 'adjacent_points: nowhere')
        self.assertItemsEqual(go.adjacent_points(18,18), [(18,17),(17,18)], 'adjacent_points: empty corner')
        self.assertItemsEqual(go.adjacent_points(0,1),   [(0,0)], 'adjacent_points: side')
        self.assertItemsEqual(go.adjacent_points(2,3),   [(3,3),(2,4)], 'adjacent_points: middle')




if __name__ == '__main__':
    unittest2.main()
