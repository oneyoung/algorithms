from tree import Node, Tree


class AVLTree(Tree):
    '''
    AVLTree is a typical binary search treee with an additional
    rescrition that the heights of the two child subtrees of any
    node differ by at most one.
    '''
    def sanity(self):
        try:
            assert super(AVLTree, self).sanity(), 'BST check fail'

            def check_node(node):
                if not node:  # end of tree
                    return
                # delta of two child height should <= 1
                assert self.balance(node), \
                    '%s height delta more than 1' % node.as_tree()

                check_node(node.leftChild)
                check_node(node.rightChild)

            check_node(self.rootNode)
            return True
        except AssertionError as e:
            print str(e)
            return False

    def balance(self, node):
        ''' test if a node is balance in AVL rule '''
        left = node.leftChild.height if node.leftChild else 0
        right = node.rightChild.height if node.rightChild else 0
        return abs(left - right) <= 1

    def fixup(self, node):
        if node.parent and node.parent.parent:
            N = node
            P = node.parent
            G = P.parent
            branch = lambda p, c: 'left' if p.leftChild == c else 'right'
            if not self.balance(G):
                # unbalance node found.
                # N is the node which has one extra height, P, G is the parent
                # and grand parent node of N. if we successfully to elimate
                # this extra height, we can stop iter to upper layer.
                # (1) if G, P, N is not at the same side, we do a rotation. now N
                # and P swap in graph (2)
                #        G                 G
                #       / \               / \
                #      P   a   --->      N   a
                #     / \               / \
                #    b   N             P   d
                #       / \           / \
                #      c   d         b   c
                #                (1)
                # (2) G, P, N in the same side, we just do a rotation to elimate
                # extra 1 height
                #          G                   P
                #         / \                 /  \
                #        P   a    ---->      N    G
                #       / \                 / \   / \
                #      N   d               b   c d   a
                #     / \
                #    b   c
                #                 (2)
                if branch(G, P) != branch(P, N):
                    # case 1: G, P, N not in the same side, do a rotation.
                    self.rotate(P, branch(G, P))
                    # assign new P, N in order to move case 2
                    P, N = N, P
                # case 2
                self.rotate(G, 'right' if branch(G, P) == 'left' else 'left')
            else:
                # recursive move up until we find a unbalance node to fixup
                self.fixup(N.parent)

    def insert(self, node_or_key):
        node = node_or_key if isinstance(node_or_key, Node) else Node(node_or_key)
        if self.rootNode and not self.find(node.key):
            # insert node just like BST way
            node = self.add_as_child(self.rootNode, node)
            # fix AVLTree rules, node is always leaf
            # we assume before insert, tree has meet AVL rules, so if we insert
            # a leaf node, the only case will break rules is its parent has
            # only one child node, which increase height by one.
            has1child = lambda n: bool(n.leftChild) != bool(n.rightChild)
            if node.parent and has1child(node.parent):
                self.fixup(node)
        else:
            self.rootNode = node

    def delete(self, key):
        node = self.find(key)
        if node:
            print 'Tree: %s del %s' % (self.rootNode.as_tree(), node)
            node, child = self.delete_node(node)
            # find the bottom node after deletion. Note there is only two case
            # after deletion(see delete_node's comment).
            # 1. leaf node is deleted, child is None
            # 2. a node with only child is deleted.

            P = child.parent if child else node.parent
            if not P:
                return
            if not self.balance(P):
                N = P
                while N.is_leaf():
                    if N.leftChild.height > N.rightChild.height:
                        N = N.leftChild
                    else:
                        N = N.rightChild
                self.fixup(N)
            return
            # find the node which break the AVL rules, then we can simply call
            # fixup to rebalance tree.
            if child:
                # in delete_node case 2 or 3, deleted node has one child.
                # X is node to be deleted, P is X's parent.
                # in this case, P must has two children, otherwise, it would
                # conflict AVL tree rule. so such deletion still keep tree
                # property, do nothing.
                #        |                       |
                #        P                       P
                #       / \                     / \
                #      c   X       ----->      c   c'
                #     / \   \                 / \
                #    a   b   c'              a   b
                P = child.parent
                pass
            else:  # deleted node is a leaf
                #           |                   |
                #           P                   P
                #          / \     ----->      /
                #         c   X               c
                P = node.parent
                if not P:
                    return
                c = P.leftChild if P.leftChild else P.rightChild
                if not c:
                    # if X is the only child of P, height decrease by 1, do a
                    # fixup on P
                    self.fixup(P)
                elif c.height == 1:
                    # c & X are two leaf of P, so deleted X would not change
                    # height of P
                    pass
                else:
                    # c has a height of 2, delete X make P unbalance.
                    #           |                         |
                    #           P                         c
                    #          /                         / \
                    #         c           ------>       c0  P
                    #        / \                             \
                    #       c0  c1                           c1
                    # we can do a rotation on P to archive balance on P.

                    branch = lambda p, c: 'left' if p.leftChild == c else 'right'
                    if c.leftChild and c.rightChild:
                        # c has both two children, a rotation would NOT change
                        # height of c(new P), so upper subtree don't change,
                        # we can stop here.
                        self.rotate(P, 'right' if P.leftChild == c else 'left')
                    else:
                        # if c has only one child, we should make sure P, c and c's
                        # child in the same side, otherwise, a rotation would not
                        # fixup the height
                        cc = c.leftChild if c.leftChild else c.rightChild
                        if branch(P, c) != branch(c, cc):  # not same side
                            #           |                         |
                            #           P                         P
                            #          /                         /
                            #         c           ------>       cc
                            #          \                       /
                            #           cc                    c
                            P.leftChild, P.rightChild = None, None
                            c.leftChild, c.rightChild = None, None
                            self.add_as_child(P, cc)
                            self.add_as_child(cc, c)
                            c, cc = cc, c
                        self.rotate(P, 'right' if P.leftChild == c else 'left')
                        # c(new P) height has changed, do fixup
                        self.fixup(c)
