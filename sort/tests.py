import unittest
import time
import random
from copy import deepcopy
import sort


class TestSort(unittest.TestCase):
    def setUp(self):
        self.funcs = ['insert_sort',
                      'merge_sort',
                      'quick_sort',
                      'counting_sort',
                      'radix_sort',
                      'quick_sort2', ]

    def get_func(self, func):
        return sort.__dict__[func]

    def test_sanity(self):
        ilist = [2, 4, 1, 9, 7, 5, 3, 2, 3]
        olist = [1, 2, 2, 3, 3, 4, 5, 7, 9]

        for func in self.funcs:
            result = self.get_func(func)(deepcopy(ilist))
            self.assertListEqual(result, olist)

    def test_runingtime(self):
        def record_time(func, array):
            start = time.time()
            func(array)
            end = time.time()

            return end - start

        # we might meet max recursion limit, set to a bigger value
        import sys
        sys.setrecursionlimit(99999)

        array0 = range(5000)
        random.shuffle(array0)

        for func in self.funcs:
            array = deepcopy(array0)
            print 'method %s spend %s' % (func, record_time(self.get_func(func), array))

        array = deepcopy(array0)
        print 'method %s spend %s' % ('list.sort', record_time(list.sort, array))
