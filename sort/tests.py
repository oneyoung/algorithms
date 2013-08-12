import unittest
from copy import deepcopy
import sort


class TestSort(unittest.TestCase):
    def test_sanity(self):
        ilist = [2, 4, 1, 9, 7, 5, 3]
        olist = [1, 2, 3, 4, 5, 7, 9]

        self.assertListEqual(sort.insert_sort(deepcopy(ilist)), olist)
        self.assertListEqual(sort.merge_sort(deepcopy(ilist)), olist)
        self.assertListEqual(sort.quick_sort(deepcopy(ilist)), olist)
