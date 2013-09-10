class BNode(object):
    def __init__(self, k):
        if k < 2:
            raise ValueError('k must bigger than 1')
        self.k = k
        # key0 <= key1 <= key2 .... <= keyn
        self.keys = []
        self.childs = []
        self.leaf = False
        self.parent = None

    def is_full(self):
        return len(self.keys) == 2 * self.k - 1

    def is_min_filled(self):
        ''' whether size of node just reach min size limit '''
        return len(self.keys) == self.k - 1

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
    def underflow(self):
        # for non root node, should has at least k - 1 nodes
        # root node, parent is None
        return self.parent and len(self.keys) < self.k - 1

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
            assert len_keys <= 2 * k - 1, 'too many keys %s' % node.keys
            # for non root node, should has at least k - 1 nodes
            if node != self.rootNode:
                assert len_keys >= k - 1, 'too few keys'
            # keys check, each keys should >= previous key
            prev = n
            for key in node.keys:
                assert key >= prev, 'key %s smaller than prev %s' % (key, prev)
                prev = key
            m >= node.keys[-1]  # last key should smaller than max

            # parent node check
            if node.parent:
                i = 0
                # if we not found, it would raise a exception
                while node.parent.childs[i] != node:
                    i += 1

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
        # update parent pointer
        node.parent = parent
        new.parent = parent
        for c in new.childs:
            c.parent = new

        # update parent node
        # node is the index rank child of the parent, so each key in node,
        # there has parent.keys[index - 1] <= key <= parent.keys[index], we
        # insert pkey before index would keep the property.
        parent.keys.insert(index, pkey)  # insert pkey to parent
        # the right place for new node is index + 1 in parent.childs.
        parent.childs.insert(index + 1, new)  # insert new node to parent's childs

    def delete(self, key):
        # first find the node which holds the key
        node = self.rootNode
        while True:
            i = 0
            while i < len(node.keys):
                if node.keys[i] >= key:  # find a suitalbe slot
                    break
                i += 1
            if i < len(node.keys) and node.keys[i] == key:  # exactly match
                break
            elif node.leaf:  # already bottom, not found
                # nothing to do, just return
                return
            else:  # traverse to child level
                node = node.childs[i]
        # in the end, key is in ith rank of node

        def delete_node(node, i):
            if node.leaf:
                # delete a key from leaf node, just do it
                node.keys.pop(i)
                return node
            else:
                # delete from a internal node
                # a internal node acts as a separator of two subtrees, if we want
                # to delete it, need to choose a new sperator(either max of left
                # node or min of right child node), have a swap between new
                # sperator and key to be delete, RBTree property keeps.
                child = node.childs[i]  # here, we choose max of left node
                while not child.leaf:  # find until reach leaf, that is max
                    child = child.childs[-1]
                node.keys[i], child.keys[-1] = child.keys[-1], node.keys[i]  # swap
                child.keys.pop(-1)  # remove that key
                node = child
            return node

        def rebalance(node):
            # if we meet the root
            if not node.parent:
                if len(node.keys) == 0:  # rootNode is empty
                    if node.childs:
                        # in case root node is empty, we move its
                        # only child up as new root
                        newRoot = node.childs[0]
                        newRoot.parent = None
                        self.rootNode = newRoot
                    else:
                        # Tree is empty
                        self.rootNode = None
            # only if node is *underflow*, we need fixup
            elif node.underflow:
                # find node's siblings
                parent = node.parent
                i = 0
                while parent.childs[i] != node:
                    i += 1
                left = parent.childs[i - 1] if i > 0 else None
                right = parent.childs[i + 1] if i < len(parent.keys) else None

                # case 1. If the deficient node's right sibling exists and has more
                # than the minimum number of elements, then rotate left
                if right and not right.is_min_filled():
                    # in order to stuff node to desired limit, the idea here is
                    # to move one key from sibling to the node, then tree
                    # balanced
                    i_parent = i  # parent of node and its right sibling
                    # left rotate: parent key move to its left child(node) end, and
                    # min of right child move to parent
                    node.keys.append(parent.keys[i_parent])
                    parent.keys[i_parent] = right.keys.pop(0)
                    # fixup child pointer is not leaf
                    if not node.leaf:
                        rc = right.childs.pop(0)
                        node.childs.append(rc)
                        rc.parent = node
                # case 2. If the deficient node's left sibling
                # exists and has more than the minimum number of elements, then
                # rotate right
                elif left and not left.is_min_filled():
                    i_parent = i - 1  # parent of node and its left sibling
                    # right rotate: parent key move to start of its right
                    # child, and max of left child move to parent
                    node.keys.insert(0, parent.keys[i_parent])
                    parent.keys[i_parent] = left.keys.pop(-1)
                    # fixup child pointer
                    if not node.leaf:
                        lc = left.childs.pop(-1)
                        node.childs.insert(0, lc)
                        lc.parent = node
                # case 3. all its sibling only meet the min limit.
                # Idea, merge node with one of its sibling:
                # this will remove one parent key. so parent becomes the
                # deficited node, we a recursive.
                else:
                    # also note that left or right child can be None, but at
                    # least one exists
                    if left:  # has left child
                        i_parent = i - 1
                        k_parent = parent.keys.pop(i_parent)  # remove parent key
                        parent.childs.pop(i)  # remove node
                        # merge to left child
                        left.keys = left.keys + [k_parent] + node.keys
                        left.childs = left.childs + node.childs
                        # update node.childs' father
                        if not node.leaf:
                            for c in node.childs:
                                c.parent = left
                    else:  # has right child
                        i_parent = i
                        k_parent = parent.keys.pop(i_parent)
                        parent.childs.pop(i)
                        # merge to right child
                        right.keys = node.keys + [k_parent] + right.keys
                        right.childs = node.childs + right.childs
                        # update node.childs' father
                        if not node.leaf:
                            for c in node.childs:
                                c.parent = right
                    rebalance(parent)  # recursive to parent node

        node = delete_node(node, i)
        # now, node must be a leaf, if num of keys less than min
        # request(underflow), or rootNode is empty, we must do rebalance.
        rebalance(node)

    def as_list(self):
        def node2list(node):
            if node.leaf:
                return node.keys
            else:
                return sum([node2list(node.childs[i]) + [node.keys[i]]
                            for i in xrange(len(node.keys))], []) + node2list(node.childs[-1])
        return node2list(self.rootNode) if self.rootNode else []
