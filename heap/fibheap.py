class Node(object):
    def __init__(self, key=None):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

    def __str__(self):
        left = self.left.key if self.left and self.left != self else ''
        right = self.right.key if self.right and self.right != self else ''
        return "[%s<%s(%s)>%s]" % (left, self.key, self.degree, right)


def dlink2list(node):
    ''' turn double linked node into a list '''
    l = []
    if node:
        start = current = node
        while 1:
            l.append(current)
            current = current.right
            if current == start:
                break
    return l


def dlink_print(node):
    l = dlink2list(node)
    print ' '.join(map(lambda n: str(n), l))


class FibHeap(object):
    def __init__(self, keys=[]):
        self.min = None
        self.num = 0  # num of nodes in heap
        for key in keys:
            self.insert(key)

    def sanity(self):
        if not self.min:  # empty heap
            return True

        def check_node(node, first=False):
            self._num_nodes += 1
            assert minval <= node.key, 'key small than minval'
            if node.parent:  # check parent node
                assert node.key > node.parent.key, 'child key small than parent'
            # check sibling
            if first:
                for sibling in dlink2list(node):
                    if sibling != node:  # avoid endless check_node(node)
                        check_node(sibling)
            # check chld node
            assert len(dlink2list(node.child)) == node.degree, 'degree not match child num'
            if node.child:
                check_node(node.child, True)

        try:
            minval = self.min.key
            self._num_nodes = 0
            check_node(self.min, True)
            assert self._num_nodes == self.num, 'num of nodes not match'
            return True
        except AssertionError as e:
            print str(e)
            return False

    @staticmethod
    def _insert_node(node, where):
        ''' insert a node in right side of where '''
        node.right.left = where.left
        old_right = node.right
        node.right = where
        where.left.right = old_right
        where.left = node

    def _root_add(self, node):
        ''' add a double linked node into head '''
        if not self.min:  # heap is empty
            self.min = node
            node.left = node.right = node
        else:  # insert node as self.min right node
            self._insert_node(node, self.min)
        for n in dlink2list(node):  # make sure every node added has no parent
            n.parent = None

    @staticmethod
    def _remove_node(node, destory=True):
        ''' remove node '''
        left, right = node.left, node.right
        if left != right:  # node has sibling
            left.right = right
            right.left = left
        if destory:
            node.left = node.right = None
        else:
            node.left = node.right = node

    def insert(self, key):
        ''' insert a key to heap '''
        node = Node(key)
        self._root_add(node)
        if self.min is None or node.key < self.min.key:
            self.min = node
        self.num += 1

    def union(self, heap):
        ''' union heap to self '''
        # add heap to self
        self._root_add(heap.min)
        # update min node
        if self.min is None or self.min.key > heap.min.key:
            self.min = heap.min
        self.num += heap.num

    def _consolidate(self):
        def link(sub, master):
            ''' add sub as a child of master '''
            #self._remove_node(sub, False)  # remove from rootlist
            # add to master
            if master.child:  # master has child, just do a insert
                self._insert_node(sub, master.child)
            else:  # master has no child
                master.child = sub
            sub.parent = master
            master.degree += 1

        import math
        size = int(math.ceil(math.log(self.num, 2)))
        # we concrete a array such that ith element has i degree node, and
        # element all belongs to rootlist.
        array = [None] * size
        for current in dlink2list(self.min):
            self._remove_node(current, False)  # remove from rootlist
            x = current
            d = x.degree
            # the idea here is to merge rootlist which has the same degree
            while array[d]:
                y = array[d]
                # x and y have the same degree, merge them
                # x would be the parent of y
                if x.key > y.key:
                    # should not merely exchange key of x & y, since the child
                    # key might smaller than parent after exchange
                    x, y = y, x
                link(y, x)
                # now x has d+1 degree
                # y is remove from rootlist, so array[d] is empty
                array[d] = None
                d += 1  # move to next loop
            array[d] = x

        self.min = None
        for node in filter(None, array):
            self._root_add(node)
            if self.min.key > node.key:
                self.min = node

    def extract_min(self):
        ''' extract min node from heap '''
        min_node = self.min
        child = min_node.child
        # add each child of min into root list
        # since childs is double linked, so just add one child to rootlist
        # would finish the work
        if child:
            self._root_add(child)
        if min_node == min_node.right:  # only min_node left
            self.min = None
        else:
            # this is not the real min node, we just want this as a node to be
            # traverse in consolidate
            self.min = min_node.right
        self._remove_node(min_node)
        if self.min:
            self._consolidate()
        self.num -= 1

        return min_node
