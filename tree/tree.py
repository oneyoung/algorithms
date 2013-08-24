class Node(object):
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.leftChild = None
        self.rightChild = None

    def __str__(self):
        return str(self.key) + "(" + str(self.height) + ")"

    @property
    def height(self):
        def depth(node, h):
            if not node:  # leaf
                return h
            else:
                return h + 1 + max(depth(node.leftChild, h),
                                   depth(node.rightChild, h))
        return depth(self, 0)

    def is_leaf(self):
        return (self.height == 0)

    def as_tree(self):
        if self.is_leaf():
            return str(self)
        else:
            left = self.leftChild.as_tree() if self.leftChild else self.leftChild
            right = self.rightChild.as_tree() if self.rightChild else self.rightChild
            if left or right:
                return str(self) + '[%s|%s]' % (left, right)
            else:
                return str(self)

    def balance(self):
        return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)


class Tree(object):
    def __init__(self, keys=[]):
        self.rootNode = None
        for key in keys:
            self.insert(key)

    def insert(self, key):
        '''override this function'''
        pass

    def height(self):
        return self.rootNode.height if self.rootNode else 0

    def find_subtree(self, node, key):
        if not node:  # key not found
            return None
        elif key < node.key:
            return self.find_subtree(node.leftChild, key)
        elif key > node.key:
            return self.find_subtree(node.rightChild, key)
        else:
            return node  # key equal

    def find_subtree2(self, key):
        ''' non-recursive version '''
        node = self.rootNode
        while node and node.key != key:
            if key < node.key:
                node = node.leftChild
            else:
                node = node.rightChild
        return node

    def find(self, key):
        #return self.find_subtree(self.rootNode, key)
        return self.find_subtree2(key)

    def _max(self, node):
        if not node:  # empty tree
            return None
        while node.rightChild:
            node = node.rightChild
        return node

    def _min(self, node):
        if not node:  # empty tree
            return None
        while node.leftChild:
            node = node.leftChild
        return node

    def max(self):
        return self._max(self.rootNode)

    def min(self):
        return self._min(self.rootNode)

    def successor(self, key):
        node = self.find(key)
        if not node:
            return None
        elif node.rightChild:  # has right child, then find the min one
            return self._min(node.rightChild)
        else:
            # search upward, until node is leftChild of its parent, or reach
            # root node. The parent is the successor
            while node.parent and node != node.parent.leftChild:
                node = node.parent
            # if node is root, we should return node instead of its parent
            return node.parent if node.parent else node

    def predecessor(self, key):
        # much like successor
        node = self.find(key)
        if not node:
            return None
        elif node.leftChild:
            return self._max(node.leftChild)
        else:
            while node.parent and node != node.parent.rightChild:
                node = node.parent
            return node.parent if node.parent else node

    def inorder(self, node):
        ret = []
        if node.leftChild:
            ret += self.inorder(node.leftChild)
        ret += [node]
        if node.rightChild:
            ret += self.inorder(node.rightChild)
        return ret

    def as_list(self):
        return self.inorder(self.rootNode) if self.rootNode else []

    def sanity(self):
        ''' check if remain the binary tree property '''
        def node_cmp(node1, node2, ops):
            if not node1 or not node2:
                return True
            else:
                return eval("%d %s 0" % (cmp(node1.key, node2.key), ops))

        def check_parent(node):
            ''' node must not be None '''
            return (node.leftChild.parent == node if node.leftChild else True) and \
                (node.rightChild.parent == node if node.rightChild else True)

        def check_subnode(node):
            if node is not None:  # we also want to check nil node
                assert node_cmp(node, node.leftChild, '>'), \
                    '%s illegal leftChild %s' % (node, node.leftChild)
                assert node_cmp(node, node.rightChild, '<'), \
                    '%s illegal rightChild %s' % (node, node.rightChild)
                assert check_parent(node), '%s illegal as parent node' % node
                check_subnode(node.leftChild)
                check_subnode(node.rightChild)

        try:
            check_subnode(self.rootNode)
            return True
        except AssertionError as e:
            print 'Tree:', self.rootNode.as_tree()
            print str(e)
            return False

    def add_as_child(self, parent, node):
        child_name = 'leftChild' if node.key < parent.key else 'rightChild'
        child_node = getattr(parent, child_name)
        if not child_node:  # child is none, we can place node here
            setattr(parent, child_name, node)
            node.parent = parent
        else:
            self.add_as_child(child_node, node)
        return node

    def replace(self, old_child, new_child):
        '''
        replace old_child with new_child
        '''
        parent = old_child.parent
        if parent:
            if parent.key > old_child.key:  # left child
                parent.leftChild = new_child
            else:
                parent.rightChild = new_child
        else:  # old_child is root node
            self.rootNode = new_child
        if new_child is not None:
            # update parent is necessary, compatible with Nil node
            new_child.parent = parent

    def rotate(self, key_or_node, dirt='right'):
        ''' right/left rotate node
        para:
            node -- upper node to be rotated
            dirt -- direction, left/right
        '''
        node = key_or_node if isinstance(key_or_node, Node) \
            else self.find(key_or_node)
        #       P                   P
        #       |                   |
        #       B      right        A
        #      / \     ------>     / \
        #     A   c    <------    a   B
        #    / \        left         / \
        #   a   b                   b   c
        child_branch, b_branch = ('leftChild', 'rightChild') if dirt == 'right' \
            else ('rightChild', 'leftChild')
        child = getattr(node, child_branch)
        assert child  # child should exists
        # get b node in above figure
        b = getattr(child, b_branch)
        # swap A & B, take right rotate for example
        # node is B, and child is A
        self.replace(node, child)  # delete B (right rotate)
        # here is tricky part, what is b is nil
        setattr(child, b_branch, node)
        node.parent = child
        setattr(node, child_branch, b)
        if b:
            b.parent = node

    def delete_node(self, node):
        ''' delete one node from tree
        return node deleted and its child who replace the node
        '''
        if (not node.rightChild) or (not node.leftChild):
            # case 1: node is left, just delete it.
            # Note: in order to complicate with nil node, we should not just
            # replace with None, its child instead
            # case 2: just has one child, replace current with its child

            # in fact, we can merge case 1 & 2 into just one routine
            child = node.rightChild if node.rightChild else node.leftChild
            self.replace(node, child)
        else:
            # case 3: has both children
            # swap key with one's successor don't change the BST property.
            # so delete successor with key exchanged instead. And it turn to
            # the same as case 2
            successor = self.successor(node.key)
            # del successor (the successor only rightChild, so replace this
            # child equal to del successor)
            self.replace(successor, successor.rightChild)
            # !!!Note: we should swap key after replacement, since such action
            # will break the Tree property
            node.key, successor.key = successor.key, node.key
            # fill return value
            node = successor
            child = successor.rightChild
        return (node, child)


class BinarySearchTree(Tree):
    def insert(self, node_or_key):
        node = node_or_key if isinstance(node_or_key, Node) else Node(node_or_key)
        if self.rootNode:
            if not self.find(node.key):  # avoid duplicated add
                self.add_as_child(self.rootNode, node)
        else:
            self.rootNode = node

    def delete(self, key):
        node = self.find(key)
        if node:
            self.delete_node(node)
        else:  # node not found
            return
