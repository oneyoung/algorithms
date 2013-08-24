from tree import Node, Tree


class RBNode(Node):
    def __init__(self, key, color='R'):
        self.color = color  # 'B' -- Black node, 'R' -- Red node
        super(RBNode, self).__init__(key)
        # for a non-nil node, it should has two nil children at init
        if not self.is_nil():
            self.leftChild = RBNode(None, color='B')
            self.leftChild.parent = self
            self.rightChild = RBNode(None, color='B')
            self.rightChild.parent = self

    def __nonzero__(self):
        '''
        in order to compliant with Tree, for nil node,
        it should test as False.
        '''
        return False if self.is_nil() else True

    def __str__(self):
        return str(self.key) + "(%s.%s)" % (self.color, str(self.height))

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

    def is_balance(self):
        if self.leftChild.bheight != self.rightChild.bheight:
            print self.as_tree()


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
            self.insert_fixup(node)

    def insert_fixup(self, node):
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
                self.insert_fixup(G)
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

    def delete(self, key):
        node = self.find(key)
        if node:
            # first, we just do deletion in Binary Search Tree.
            # Note: the node returned by delete_node might not be the exactly
            # node we pass, since in case 3, it exchange with successor
            # Note2: for the child, is the one who replace the node. Except the
            # situation that node is leaf(case 1), the deleted node has only one child
            # (in case 3, we exchange with successor who has only one child)
            node, child = self.delete_node(node)
            # If deleted node's color is Red, all properties still stand.
            # * Black height of all subtree not change
            # * Red node with a red child does not exists
            # * Red node can't be root, so root still be black
            # The real problem is when a black node is gone
            # We need a fixup here to maintain Red-Black property.
            if node.color == 'B':
                self.delete_fixup(child)
        else:  # key not found
            return

    def delete_fixup(self, node):
        x = node
        # The problem is when the deleted node is black, the black height of
        # all subtrees through x(child of deleted node) shirink by 1.
        # So the fix is to find a way to add one black height to this path.

        # after each loop end, we always keep the top node the same color. So
        # upper subtree always keep RB-property, so does the down subtree.
        # the only problem is in x node, it has an extra black height.
        # **Once when x's color is Red, we are lucky enough to stop while loop.
        # just paint the x to black, that means x's black height add 1.
        # and for red node, its parent and child must be black, so 3 black node
        # in a row still maintain RB-property.
        while x != self.rootNode and x.color == 'B':
            # we can treat x as a *Double-Black or Red-Black* node, depended by
            # the original color of x, and we add a Black color to it, in order
            # to make tree balance.
            # Note: in fact, the color of x does not actually change, we just
            # look at it just having an extra black color in notion.
            p = x.parent
            # **we assume x is the left child
            # since the options is symatic, we use the below strategy to make
            # options clear while support both side situation.
            if x == p.leftChild:
                left, right = ('left', 'right')
                leftChild, rightChild = ('leftChild', 'rightChild')
            else:
                left, right = ('right', 'left')
                leftChild, rightChild = ('rightChild', 'leftChild')
            # **sibling of x should exists since black height of x is at least 2.
            # 1. if x original color is Red, that means it has at least a black
            # child, adding the deleted black father, height at least 2.
            # 2. if x original color is Black, x is double-black
            s = getattr(p, rightChild)  # sibling of x

            if s.color == 'R':
                # case 1: sibling s is Red
                # that means s must have 2 black child, and p is black
                # we can swap color between s and p, and do a left rotate
                #     B(p)                              D
                #    / \       left rotate             / \
                #(x)A   D.(s)  ----------->           B.  E
                #      / \                           / \
                #     C   E                      (x)A   C(s)
                # (symbal notation:
                #   '.' -- Red,
                #   '*' -- Red/Black,
                #   '' -- Black)
                # then we can move to next, since new sibling of x is black
                s.color, p.color = p.color, s.color
                self.rotate(p, left)
            else:  # sibling is black
                s_leftChild = getattr(s, leftChild)
                s_rightChild = getattr(s, rightChild)

                if s_leftChild.color == 'B' and s_rightChild.color == 'B':
                    # case2: s is black, and has two black child
                    #       B*(p)                    (new x)  B (BB, or RB)
                    #      / \       re-color                / \
                    #  (x)A   D(s)   ----------->           A   D.
                    #        / \                               / \
                    #       C   E                             C   E
                    # we can have a re-color options here. and move upwards.
                    # 1. x and s minus one Black color. (x is BB or RB
                    # originally, so after ops, it become a normal node; s has
                    # two black node, so paint it as red has no problem)
                    # 2. in order to make upper tree balance, we need to add a
                    # black color to parent node p ==> that means p becomes a
                    # new x node with BB/RB color, we can continue the loop.
                    # Note: if we enter from case1, B is red, so new x is red,
                    # then next loop will terminated.
                    s.color = 'R'
                    x = p
                elif s_leftChild.color == 'R':
                    # case 3: s is black, and has a Red left child
                    #       B*(p)                     B*(p)
                    #      / \                       / \
                    #  (x)A   D(s)    ------->   (x)A   C(new s)
                    #        / \                         \
                    #       C.  E                         D.
                    #                                      \
                    #                                       E
                    # we can swap color with s and its leftChild, then do a
                    # right rotation, RB-property still be true. It turns out
                    # to be the sitatution of case 4, s has a Red rightChild
                    s.color = 'R'
                    s_leftChild.color = 'B'
                    self.rotate(s, right)
                else:
                    # case 4: s is black, and has a Red right child
                    #      B*(p)                  D              D*
                    #     / \                    / \  re-color  / \
                    # (x)A   D(s)   ------>     B*  E. ---->   B   E
                    #       / \                / \             / \
                    #      C*  E.             A   C*          A   C*
                    # do a left rotate, and recolor
                    # we finally can decrease a black color in both side, DONE
                    self.rotate(p, left)
                    s.color = p.color
                    p.color = 'B'
                    s_rightChild.color = 'B'
                    # done, terminate
                    x = self.rootNode
        x.color = 'B'

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
                node.is_balance()
                assert node.leftChild.bheight == node.rightChild.bheight, '%s subtree has diff height' % node
                # Every red node must have two black child nodes.
                if node.color == 'R':
                    assert node.leftChild.color == 'B', '%s left child is not black' % node
                    assert node.rightChild.color == 'B', '%s right child is not black' % node
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
