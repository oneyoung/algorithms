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
        else:
            self.add_as_child(child_node, node)

    def insert(self, node):
        if self.rootNode:
            if not self.find(node.key):  # avoid duplicated add
                self.add_as_child(self.rootNode, node)
        else:
            self.rootNode = node

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

    def find(self, key):
        return self.find_subtree(self.rootNode, key)

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
