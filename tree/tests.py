import unittest


class TestTree(unittest.TestCase):
    def test_sanity(self):
        def check_tree_sanity(cls):
            array = [2, 3, 1, 7, 9, 5, 6, 11]
            array_sorted = [1, 2, 3, 5, 6, 7, 9, 11]
            t = cls(array)
            self.assertTrue(t.sanity())
            #self.assertEqual(t.height(), 5)
            self.assertListEqual([n.key for n in t.as_list()], array_sorted)
            self.assertEqual(t.max().key, 11)
            self.assertEqual(t.min().key, 1)
            # test predecessor and successor
            for i in range(len(array_sorted)):
                if i != 0:  # test predecessor
                    self.assertEqual(t.predecessor(array_sorted[i]).key,
                                     array_sorted[i - 1])
                if i != len(array_sorted) - 1:  # test successor
                    self.assertEqual(t.successor(array_sorted[i]).key,
                                     array_sorted[i + 1])

            # inster & deletion test
            length = len(t.as_list())
            key = 4
            t.insert(key)
            self.assertTrue(t.sanity())
            self.assertEqual(length + 1, len(t.as_list()))
            self.assertTrue(t.find(key))

            key = 5
            t.delete(key)
            self.assertTrue(t.sanity())
            self.assertEqual(length, len(t.as_list()))
            self.assertFalse(t.find(key))  # key should gone

            key = 7
            t.delete(key)
            self.assertTrue(t.sanity())
            self.assertEqual(length - 1, len(t.as_list()))
            self.assertFalse(t.find(key))

        from tree import BinarySearchTree
        check_tree_sanity(BinarySearchTree)
        # test rotate
        t = BinarySearchTree([10, 7, 5, 8, 4, 6])
        t.rotate(7, 'right')
        self.assertEqual(6, len(t.as_list()))
        self.assertTrue(t.sanity())
        t.rotate(5, 'left')
        self.assertEqual(6, len(t.as_list()))
        self.assertTrue(t.sanity())
        from rbtree import RBTree
        check_tree_sanity(RBTree)
