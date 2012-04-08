#!/usr/bin/python
import unittest
import sys
sys.path.append("")

from go.goobject import GoObject


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
    }



class BasicAccess(unittest.TestCase):
    def runTest(self):
        go = GoObject()
        go.board = boards["white_only"].copy()

        self.assertEqual( len(go), 14, "len" )
        self.assertEqual( go[2,3], w,     "Getter" )
        self.assertEqual( go[0,0], None,  "Getter for non-existant" )
        self.assertRaises( IndexError, lambda x: go[19,19], "getter: IndexError when out of bounds" )

        go[0,0] = w
        def python_lambdas_suck_1(x):
            go[19,19] = w
        self.assertEqual( go[0,0], w,     "Setter" )
        self.assertRaises( IndexError, python_lambdas_suck_1, "setter: IndexError when out of bounds" )

        del go[2,3]
        self.assertEqual( go[2,3], None,  "del" )
        def python_lambdas_suck_2(x):
            del go[19,19]
        self.assertRaises( IndexError, python_lambdas_suck_2, "del: IndexError when out of bounds" )

        self.assertTrue(  (3,4)   in go,     "__contains__" )
        self.assertFalse( (3,1)   in go,     "not __contains__" )
        self.assertFalse( (19,19) in go,     "__contains__ out of bounds" )

        self.assertEqual( go.get(3,4, 42), w, "get() existing" )
        self.assertEqual( go.get(9,9, 42), 42, "get() non-existing" )
        self.assertEqual( go.get(19,19, 42), 42, "get() out of bounds" )



class TestGrouping(unittest.TestCase):
    """
python -mtimeit \
-s 'from goobject import GoObject' \
-s 'class S(object): pass' \
-s 'w = S()' \
-s 'w.stone_color = "white"' \
-s 'go = GoObject()' \
-s 'go.board = {(1,0):w,(1,1):w,(2,1):w,(2,2):w,(0,3):w,(1,3):w,(2,3):w,(3,3):w,(1,4):w,(2,4):w,(3,4):w,(1,5):w,(2,5):w,(3,5):w}'  \
'go.get_group(2,3)'
   """

    def runTest(self):
        go = GoObject()
        go.board = boards["white_only"].copy()
        the_group = sorted(boards["white_only"].keys())

        self.assertEqual(sorted(go.get_group(2,3)), the_group, 'big group from loc 1')
        self.assertEqual(sorted(go.get_group(1,0)), the_group, 'big group from loc 2')
        self.assertEqual(sorted(go.get_group(0,0)), [],        'empty location w/neighbor')
        self.assertEqual(sorted(go.get_group(9,9)), [],        'empty location no neighbors')




if __name__ == '__main__':
    unittest.main()
