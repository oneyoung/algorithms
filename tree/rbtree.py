from tree import Node, Tree


class RBNode(Node):
    def __init__(self, key, color='R'):
        self.color = color  # 'B' -- Black node, 'R' -- Red node
        super(RBNode, self).__init__(key)
        # for a non-nil node, it should has two nil children at init
        if not self.is_nil():
            self.leftChild = nil
            self.rightChild = nil

    def __nonzero__(self):
        '''
        in order to compliant with Tree, for nil node,
        it should test as False.
        '''
        return False if self.is_nil() else True

    def __str__(self):
        return str(self.key) + "(%s.%s)" % (self.color, str(self.height))

    def as_tree(self):
        if self.is_nil():
            return str(self)
        else:
            return str(self) + '[%s|%s]' % (self.leftChild.as_tree(), self.rightChild.as_tree())

    def is_nil(self):
        return self.key is None

    @property
    def bheight(self):
        ''' height in black node '''
        def depth(node, h):
            if node.is_nil():  # nil node
                return h + 1
            else:
                valid = 1 if node.color == 'B' else 0
                # accroding to Red-black properties, either side has the same
                # height, so we just pick leftChild now
                return h + valid + depth(node.leftChild, h)
        return depth(self, 0)

nil = RBNode(None, color='B')  # obj to present all nil node


class RBTree(Tree):
    def insert(self, key):
        node = RBNode(key, color='R')
        if self.rootNode is None:
            self.rootNode = node
            node.color = 'B'  # root node is black
        else:
            # first, insert node in BST tree
            node = self.add_as_child(self.rootNode, node)
            # fix RB-Tree proterty
            self.fix_rb_prop(node)

    def fix_rb_prop(self, node):
        N = node  # rename current node as N
        P = N.parent
        if not P:
            # case 1: N is rootNode, make sure it's black
            N.color = 'B'
        elif P.color == 'B':
            # case 2: parent is Black and child is Red,
            # all rules satisfied, do nothing
            pass
        else:
            # P is red, that means it should has a black parent
            G = P.parent  # grandparent of N
            sideP, sideU = ('rightChild', 'leftChild') if P.key > G.key else \
                ('leftChild', 'rightChild')
            U = getattr(G, sideU)  # uncle of N

            if U.color == 'R':
                # case 3: both P and U are red,
                # as N is red, we can paint P and U black,
                # so G becomes Red, that means we could treat G as a new N and
                # move upward, do the recurse
                P.color = U.color = 'B'
                G.color = 'R'
                self.fix_rb_prop(G)
            else:  # U is black while P is red
                # now we assume P is left child of G, if in right side, do
                # reverse ops
                sideN = 'leftChild' if N.key < P.key else 'rightChild'
                if sideN != sideP:
                    # case 4: N is in left side, ie, diff side with P
                    # we can do a left rotation here, so it could be turned
                    # into case 5
                    self.rotate(P, 'left' if 'left' in sideP else 'right')
                    P, N = N, P  # swap N & P
                # case 5: P is leftChild of G, N is leftChild of P
                # we can do a right rotation on G, then we fixed now
                # (Note: node with . is red node)
                #     G               P.                    P
                #    / \             / \     re-color      / \
                #   P.  U   ==>     N.  G    =======>     N.  G.
                #  / \                 / \                   / \
                # N.  X               X   U                 X   U
                # after transform, the top node is black, as the same before
                # transform, so for upper layer, it's OK
                self.rotate(G, 'right' if 'left' in sideP else 'left')
                # re-color
                P.color, G.color = G.color, P.color

    def sanity(self):
        if self.rootNode is None:  # empty Tree
            return True
        try:
            # first should satisfy Binary Search property
            assert super(RBTree, self).sanity(), 'BST rule not satisfied'

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
                assert node.leftChild.bheight == node.rightChild.bheight, '%s subtree has diff height' % node
                # Every red node must have two black child nodes.
                if node.color == 'R':
                    assert node.leftChild.color == 'B', '%s left child is not black' % node
                    assert node.rightChild.color == 'B', '% right child is not black' % node
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
