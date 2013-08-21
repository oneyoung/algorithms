from tree import Node, Tree


class NodeRB(Node):
    def __init__(self, key):
        self.color = 'B'  # 'B' -- Black node, 'R' -- Red node
        super(Node, self).__init__(key)

    def __nonzero__(self):
        '''
        in order to compliant with Tree, for nil node,
        it should test as False.
        '''
        return False if self.is_nil() else True

    def __str__(self):
        return str(self.key) + "(%s.%s)" % (self.color, str(self.height))

    def is_nil(self):
        return not(self.key is None)

    @property
    def bheight(self):
        ''' height in black node '''
        def depth(node, h):
            if node.is_nil():  # nil node
                return h + 1
            else:
                valid = 1 if self.color == 'B' else 0
                # accroding to Red-black properties, either side has the same
                # height, so we just pick leftChild now
                return h + valid + depth(node.leftChild, h)
        return depth(self, 0)

nil = NodeRB(None)  # obj to present all nil node


class RBTree(Tree):
    def sanity(self):
        if self.rootNode is None:  # empty Tree
            return True
        try:
            # first should satisfy Binary Search property
            assert super(Tree, self).sanity(), 'BST rule not satisfied'

            # test RB-Tree property
            def check_node(node):
                # all node should not be None, nil is another case
                assert node is not None, 'node is None'
                # A node is either red or black.
                assert node.color == 'B' or node.color == 'R', 'node with wrong color'
                # All leaves (NIL) are black.
                if node.is_nil():
                    assert node.color == 'B', 'nil node is not black'
                    return  # nil indicate leaf of Tree
                # Every simple path from a given node to any of its descendant
                # leaves contains the same number of black nodes.
                assert node.leftChild.bheight == node.rightChild.bheight, 'subtree has diff height'
                # Every red node must have two black child nodes.
                if node.color == 'R':
                    assert node.leftChild.color == 'B', 'left child is not black'
                    assert node.rightChild.color == 'B', 'right child is not black'
                # traverse subnode
                check_node(node.leftChild)
                check_node(node.rightChild)

            # rootNode must be Black
            assert self.rootNode.color == 'B', 'rootNode is not black'
            check_node(self.rootNode)
            return True
        except AssertionError as e:
            print (str(e))
            return False
