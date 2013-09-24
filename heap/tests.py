import unittest
from copy import deepcopy
import random


class TestHeap(unittest.TestCase):
    def check_sorted(self, array):
        prev = array[0]
        for i in range(len(array)):
            assert prev <= array[i], \
                '%s: index %s smaller than previous' % (array, prev, i)

    def test_sanity(self):
        ilist = [2, 4, 1, 9, 7, 5, 3, 2, 3]
        olist = [1, 2, 2, 3, 3, 4, 5, 7, 9]
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

    def test_bheap(self):
        from bheap import BHeap
        array = range(100)
        random.shuffle(array)
        heap = BHeap(array)
        self.assertTrue(heap.sanity())

        min_node = heap.extract_min()
        self.assertEqual(0, min_node.key)
        self.assertTrue(heap.sanity())

    def test_fibheap(self):
        from fibheap import FibHeap
        array = range(100)
        random.shuffle(array)
        heap = FibHeap(array)
        self.assertTrue(heap.sanity())

        self.assertEqual(heap.extract_min().key, 0)
        self.assertTrue(heap.sanity())
        self.assertEqual(heap.extract_min().key, 1)
        self.assertTrue(heap.sanity())
        self.assertEqual(heap.extract_min().key, 2)
        self.assertTrue(heap.sanity())

        heap.insert(1023)
        self.assertTrue(heap.sanity())
        heap.insert(0)
        self.assertTrue(heap.sanity())
        self.assertEqual(heap.extract_min().key, 0)
        self.assertTrue(heap.sanity())
