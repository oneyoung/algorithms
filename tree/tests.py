import unittest


class TestTree(unittest.TestCase):
    def test_sanity(self):
        def check_tree_sanity(cls):
            array = [2, 3, 1, 7, 9, 5, 6, 11]
            t = cls(array)
            self.assertTrue(t.sanity())
            #self.assertEqual(t.height(), 5)
            self.assertListEqual([n.key for n in t.as_list()],
                                 [1, 2, 3, 5, 6, 7, 9, 11])
            self.assertEqual(t.max().key, 11)
            self.assertEqual(t.min().key, 1)
            self.assertEqual(t.successor(5).key, 6)
            self.assertEqual(t.predecessor(7).key, 6)

            # inster & deletion test
            length = len(t.as_list())
            t.insert(4)
            self.assertTrue(t.sanity())
            self.assertEqual(length + 1, len(t.as_list()))
            t.delete(5)
            self.assertTrue(t.sanity())
            self.assertEqual(length, len(t.as_list()))
            t.delete(7)
            self.assertTrue(t.sanity())
            self.assertEqual(length - 1, len(t.as_list()))

        from tree import BinarySearchTree
        check_tree_sanity(BinarySearchTree)
        # test rotate
        t = BinarySearchTree([10, 7, 5, 8, 4, 6])
        t.rotate(7, 'right')
        self.assertTrue(t.sanity())
        t.rotate(5, 'left')
        self.assertTrue(t.sanity())
        from rbtree import RBTree
        check_tree_sanity(RBTree)
