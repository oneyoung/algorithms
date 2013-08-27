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
                      'bucket_sort',
                      'quick_sort2', ]

    def get_func(self, func):
        return sort.__dict__[func]

    def check_sorted(self, array):
        prev = array[0]
        for i in range(len(array)):
            assert prev <= array[i], \
                '%s: index %s smaller than previous' % (array, prev, i)

    def test_sanity(self):
        ilist = [2, 4, 1, 9, 7, 5, 3, 2, 3]
        olist = [1, 2, 2, 3, 3, 4, 5, 7, 9]

        for func in self.funcs:
            result = self.get_func(func)(deepcopy(ilist))
            self.assertListEqual(result, olist)

        # test some misc func
        self.assertTupleEqual(sort.list_range(ilist), (1, 9))
        self.assertTupleEqual(sort.list_range([1, 9, 5, 6]), (1, 9))

        self.assertEqual(sort.randomize_select([2, 10, 8, 4, 7, -1], 3), 4)
        array = range(1, 500)
        random.shuffle(array)
        self.assertEqual(sort.randomize_select(array, 111), 111)

        array = range(500)
        random.shuffle(array)
        self.check_sorted(sort.bucket_sort(array))

        # heap test
        from heap import Heap
        h = Heap(deepcopy(ilist))
        h.sanity()
        self.assertListEqual(h.sort(), olist)
        # min heap
        h = Heap(deepcopy(ilist), htype='min')
        h.sanity()
        self.assertListEqual(h.sort(), olist[::-1])
        # big array test
        array = range(500)
        random.shuffle(array)
        h = Heap(array)
        h.sanity()
        self.check_sorted(h.sort())

        # priority queue
        from heap import PriorityQueue
        q = PriorityQueue(deepcopy(ilist))
        q.sanity()
        # get top test
        top = q.find_top()
        self.assertEqual(top, max(ilist))
        self.assertEqual(top, q.pop_top())
        q.sanity()
        self.assertNotEqual(top, q.find_top())
        # update key test
        q.update_key(3, 10)  # upwards
        q.sanity()
        q.update_key(8, 0)  # downwards
        q.sanity()
        # insert key test
        q.insert_key(15)
        q.sanity()
        q.insert_key(-1)
        q.sanity()
        q.insert_key(4)
        q.sanity()

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
