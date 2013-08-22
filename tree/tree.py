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
        else:  # search upward, until parent has a right node.
            node = node.parent
            while node and not node.rightChild:
                node = node.parent
            return node

    def predecessor(self, key):
        node = self.find(key)
        if not node:
            return None
        elif node.leftChild:
            return self._max(node.leftChild)
        else:
            node = node.parent
            while node and not node.leftChild:
                node = node.parent
            return node

    def inorder(self, node):
        ret = []
        if node.leftChild:
            ret += self.inorder(node.leftChild)
        ret += [node]
        if node.rightChild:
            ret += self.inorder(node.rightChild)
        return ret

    def as_list(self):
        return self.inorder(self.rootNode)

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
            if node:
                if not node_cmp(node, node.leftChild, '>'):
                    return False
                if not node_cmp(node, node.rightChild, '<'):
                    return False
                return check_subnode(node.leftChild) and \
                    check_subnode(node.rightChild) and \
                    check_parent(node)
            else:  # leaf
                return True

        return check_subnode(self.rootNode)

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
        if new_child:  # update parent is necessary
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
            if node.rightChild is None and node.leftChild is None:  # leaf
                self.replace(node, None)
            elif node.rightChild is None or node.leftChild is None:
                # has one child
                child = node.rightChild if node.rightChild else node.leftChild
                self.replace(node, child)
            else:  # has both children
                successor = self.successor(node.key)
                node.key = successor.key  # replace with successor
                # del successor (the successor only rightChild, so replace this
                # child equal to del successor)
                self.replace(successor, successor.rightChild)
        else:  # node not found
            return
