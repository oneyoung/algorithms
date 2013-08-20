class Node():
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

    def max_children_height(self):
        if self.leftChild and self.rightChild:
            return max(self.leftChild.height, self.rightChild.height)
        elif self.leftChild and not self.rightChild:
            return self.leftChild.height
        elif not self.leftChild and self.rightChild:
            return self.rightChild.height
        else:
            return -1

    def balance(self):
        return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)


class Tree():
    def __init__(self, nodes=[]):
        self.rootNode = None
        for node in nodes:
            self.insert(node)

    def add_as_child(self, parent, node):
        child_name = 'leftChild' if node.key < parent.key else 'rightChild'
        child_node = getattr(parent, child_name)
        if not child_node:  # child is none, we can place node here
            setattr(parent, child_name, node)
            node.parent = parent
        else:
            self.add_as_child(child_node, node)

    def insert(self, node):
        if self.rootNode:
            if not self.find(node.key):  # avoid duplicated add
                self.add_as_child(self.rootNode, node)
        else:
            self.rootNode = node

    def delete(self, key):
        def replace(old_child, new_child):
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

        node = self.find(key)
        if node:
            if node.rightChild is None and node.leftChild is None:  # leaf
                replace(node, None)
            elif node.rightChild is None or node.leftChild is None:
                # has one child
                child = node.rightChild if node.rightChild else node.leftChild
                replace(node, child)
            else:  # has both children
                successor = self.successor(node.key)
                node.key = successor.key  # replace with successor
                # del successor (the successor only rightChild, so replace this
                # child equal to del successor)
                replace(successor, successor.rightChild)
        else:  # node not found
            return

    def sanity(self):
        ''' check if remain the binary tree property '''
        def node_cmp(node1, node2, ops):
            if node1 is None or node2 is None:
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


class BinarySearchTree(Tree):
    pass
