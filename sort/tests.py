import unittest
from copy import deepcopy
import sort


class TestSort(unittest.TestCase):
    def setUp(self):
        self.funcs = ['insert_sort',
                      'merge_sort',
                      'quick_sort',
                      'quick_sort2', ]

    def test_sanity(self):
        ilist = [2, 4, 1, 9, 7, 5, 3]
        olist = [1, 2, 3, 4, 5, 7, 9]

        for func in self.funcs:
            result = sort.__dict__[func].__call__(deepcopy(ilist))
            self.assertListEqual(result, olist)
