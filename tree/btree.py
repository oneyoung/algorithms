class BNode(object):
    def __init__(self, k):
        if k < 2:
            raise ValueError('k must bigger than 1')
        self.k = k
        # k0 <= k1 <= k2 .... <= kn
        self.keys = []
        self.childs = []
        self.leaf = False

    def is_full(self):
        return len(self.keys) == 2 * self.k - 1

    def find(self, key):
        i = 0
        while i < len(self.keys):
            if self.keys[i] >= key:  # find a suitalbe slot
                break
            i += 1
        if i < len(self.keys) and self.keys[i] == key:  # exactly match
            return self.keys[i]
        elif self.leaf:  # already bottom, not found
            return None
        else:  # traverse to child level
            return self.childs[i].find(key)

    @property
    def height(self):
        node = self
        h = 1
        while not node.leaf:
            node = node.childs[0]
            h += 1
        return h


class BTree(object):
    def __init__(self, k, keys=[]):
        if k < 2:
            raise ValueError('k must bigger than 1')
        self.k = k
        self.rootNode = None
        for key in keys:
            self.insert(key)

    def alloc_node(self):
        return BNode(self.k)

    def sanity(self):
        k = self.k

        def check_node(node, n, m):
            ''' check node sanity with a range (n, m) '''
            len_keys = len(node.keys)
            len_child = len(node.childs)
            # each node has almost 2k - 1 node
            assert len_keys <= 2 * k - 1, 'too many keys'
            # for non root node, should has at least k - 1 nodes
            if node != self.rootNode:
                assert len_keys >= k - 1, 'too few keys'
            # keys check, each keys should >= previous key
            prev = n
            for key in node.keys:
                assert key >= prev, 'key %s smaller than prev %s' % (key, prev)
                prev = key
            m >= node.keys[-1]  # last key should smaller than max

            if not node.leaf:
                # all child should have less than 2k childs
                assert len_child <= 2 * k, 'too many children'
                # each node should have n(num of keys) + 1 children
                # if it's not a leaf
                assert len(node.childs) == len(node.keys) + 1, 'child nodes not match'
                # all child node should have same height
                height = node.height - 1
                for child in node.childs:
                    assert height == child.height, 'child not same height'
                # recursive check child nodes
                for i in xrange(1, len_keys):
                    check_node(node.childs[i], node.keys[i - 1], node.keys[i])
                check_node(node.childs[0], float('-inf'), node.keys[0])  # left boundary
                check_node(node.childs[-1], node.keys[-1], float('inf'))  # right boundary

        try:
            if self.rootNode:
                # if tree is not empty, rootNode should has at least one keys
                assert len(self.rootNode.keys) >= 1, 'root node has no key'
                check_node(self.rootNode, float('-inf'), float('inf'))
            return True
        except AssertionError as e:
            print str(e)
            return False

    def find(self, key):
        return self.rootNode.find(key) if self.rootNode else None

    def insert(self, key):
        def insert_nonfull(node, key):
            # premise: node is not full
            # target: we want to insert node in leaf node
            len_keys = len(node.keys)
            # find a suitable slot
            i = 0
            while i < len_keys and node.keys[i] < key:
                i += 1
            if node.leaf:
                # already a leaf, since node is not full, just insert the key
                node.keys.insert(i, key)
            else:
                # traverse to child node
                if node.childs[i].is_full():
                    # child is full, do split
                    self.split_node(node, i, node.childs[i])
                    # compare the new key, increase i if necessary
                    if key > node.keys[i]:
                        i += 1
                insert_nonfull(node.childs[i], key)

        if self.rootNode:
            r = self.rootNode
            if r.is_full():  # root node is full
                # This is the *only* way to increase tree height
                newRoot = self.alloc_node()
                newRoot.leaf = False
                newRoot.childs.append(r)  # update 0 child here
                self.rootNode = newRoot
                self.split_node(newRoot, 0, r)
                insert_nonfull(newRoot, key)
            else:
                insert_nonfull(r, key)
        else:  # empty tree
            self.rootNode = self.alloc_node()
            self.rootNode.leaf = True
            self.rootNode.keys.append(key)

    def split_node(self, parent, index, node):
        ''' split child node into two subnodes when child node is full
        node is the rank index child of the parent
        '''
        if not node.is_full():  # not full, no need to split
            return
        k = self.k
        new = self.alloc_node()
        # split node into two parts, and pop (k-1)th(0 base) elements
        lkeys, pkey, rkeys = node.keys[0: k - 1], node.keys[k - 1], node.keys[k:]
        lchild, rchild = node.childs[0: k], node.childs[k:]
        node.keys, new.keys = lkeys, rkeys
        node.childs, new.childs = lchild, rchild
        # new node has same leaf property with original
        new.leaf = node.leaf
        # update parent node
        # node is the index rank child of the parent, so each key in node,
        # there has parent.keys[index - 1] <= key <= parent.keys[index], we
        # insert pkey before index would keep the property.
        parent.keys.insert(index, pkey)  # insert pkey to parent
        # the right place for new node is index + 1 in parent.childs.
        parent.childs.insert(index + 1, new)  # insert new node to parent's childs

    def as_list(self):
        def node2list(node):
            if node.leaf:
                return node.keys
            else:
                return sum([node2list(node.childs[i]) + [node.keys[i]]
                            for i in xrange(len(node.keys))], []) + node2list(node.childs[-1])
        return node2list(self.rootNode)
