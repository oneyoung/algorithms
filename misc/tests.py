from random import randint
from unittest import TestCase


def rand():
    while True:
        yield randint(1, 182734618237419234)

rnum = rand()


class MiscTest(TestCase):
    def test_mod(self):
        from misc import mod
        from itertools import islice
        for i in xrange(100):
            n, p, m = islice(rnum, 3)
            self.assertEqual(pow(n, p, m), mod(n, p, m))
