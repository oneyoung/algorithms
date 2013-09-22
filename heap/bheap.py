class Node(object):
    def __init__(self, key=None):
        self.key = key
        self.parent = None
        self.degree = 0
        self.child = None
        self.sibling = None


class BHeap(object):
    def __init__(self):
        self.head = None

    def sanify(self):
        def check_node(node):
            # check parent node: node's key should bigger than parent's key
            if node.parent:
                assert node.key > node.parent.key, 'child key small than parent'
                # check sibling, if parent is None, it's root tree, so no need
                # to check its sibling
                if node.sibling:
                    assert node.degree == node.sibling.degree + 1, 'sibling degree not match'
                    assert node.key < node.sibling.key, 'key bigger than its sibling'
                    check_node(node.sibling)
            # check child node
            if node.degree:
                count = 0
                child = node.child
                while child:
                    count += 1
                    assert child.parent == node, 'child\'s parent pointer not match'
                    check_node(child)
                    child = child.sibling
                assert count == node.degree, 'child num not equal degree'

        node = self.head
        degree = 0
        try:
            while node:
                assert node.degree > degree, 'degree not ascending'
                check_node(node)
                node = node.sibling
            return True
        except AssertionError as e:
            print str(e)
            return False

    def min(self):
        node = self.head
        minval = float('inf')
        minNode = None
        # Binomial heap meets min-heap property, so its min key must in the
        # root list of heap.
        while node.sibling:
            if node.key < minval:
                minval = node.key
                minNode = node
            node = node.sibling
        return minNode

    def union(self, h2):
        ''' union with h2 '''

        def link(sub, master):
            ''' link two bin tree (with degree k-1) into one tree (degree k)
            such that master becomes the parent of sub
            '''
            sub.parent = master
            sub.sibling = master.child
            master.child = sub
            master.degree += 1

        def merge(h1, h2):
            ''' merge two heap h1 and h2,
            and sort its tree's degree in ascending order.

            return val: the head after merge
            '''
            # two input tree has been sorted in degree, all we need to do is to
            # merge two of them like merge sort
            head = Node()  # creat dummy head for easy appending
            newtree = head
            t1, t2 = h1.head, h2.head
            while t1 and t2:
                if t1.degree < t2.degree:
                    newtree.sibling = t1
                    t1 = t1.sibling
                else:
                    newtree.sibling = t2
                    t2 = t2.sibling
                newtree = newtree.sibling
            newtree.sibling = t1 if t1 else t2
            return head.sibling  # real head is dummy head's sibling

        def heap_union(h1, h2):
            ''' do a union between heap h1 and h2
            return the union head
            '''
            head = merge(h1, h2)
            if not head:  # empty heap
                return head
            # new heap has arrange as degree ascending ording, but there might
            # be some sibling nodes has the same degree. This is the work to
            # be handled.
            prevx = None
            x = head
            nextx = x.sibling
            while nextx:
                # case 1: nextx.degree bigger than current degree, OK, pass
                # case 2: x, and later two node has same degree, i.e. 3 node
                # has the same degree. in this case, we can merge x and nextx,
                # so new tree will have a bigger degree than prevx. We can do
                # this by move on pointer in order to enter case 3 or 4.
                if x.degree != nextx.degree or (nextx.sibling and
                                                nextx.sibling.degree == x.degree):
                    prevx = x
                    x = nextx
                # case 3: x and its sibling has same degree, sibling has bigger
                # key, just link sibling to x as its child
                elif x.key <= nextx.key:
                    x.sibling = nextx.sibling
                    link(nextx, x)
                # case 4: x and its sibling has same degree, sibling has small
                # key, we need to merge x into sibling's child.
                else:
                    if prevx is None:  # in case prevx None, so x is head
                        head = nextx
                    else:
                        prevx.sibling = nextx
                    link(x, nextx)
                nextx = x.sibling
            return head

        self.head = heap_union(self, h2)

    def insert(self, key):
        h = BHeap()
        h.head = Node(key)
        self.union(h)

    def extract_min(self):
        # delete the min node
        node = self.head
        minval = float('inf')
        minnode = None
        prev = prevmin = None
        while node.sibling:
            if node.key < minval:
                prevmin = prev
                minval = node.key
                minnode = node
            prev = node
            node = node.sibling
        if prevmin:
            prevmin.sibling = minnode.sibling
        else:  # delete the head node
            self.head = minnode.sibling

        # build the tree and reverse childs of deleted node
        childs = []
        child = minnode.child
        while child:
            child.parent = None
            child.sibling = None
            childs.append(child)
        childs.reverse()

        # build the new heap and add child to it
        dummy_head = Node()
        n = dummy_head
        for c in childs:
            n.sibling = c
            n = n.sibling
        heap = BHeap()
        heap.head = dummy_head.sibling

        # do a union
        self.union(heap)

    def decrease_key(self, node, key):
        assert key > node.key, 'new key greater than original one'
        parent = node.parent
        while parent and parent.key > node.key:
            parent.key, node.key = node.key, parent.key
            node = parent
            parent = node.parent

    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.extract_min()
