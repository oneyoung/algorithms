import unittest
from tree import Node, BinarySearchTree


class TestTree(unittest.TestCase):
    def test_sanity(self):
        array = [2, 3, 1, 7, 9, 5, 6, 11]
        t = BinarySearchTree([Node(i) for i in array])
        self.assertEqual(t.height(), 5)
        self.assertListEqual([n.key for n in t.as_list()],
                             [1, 2, 3, 5, 6, 7, 9, 11])
