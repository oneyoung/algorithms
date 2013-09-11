from tree import Node, Tree


class ANode(Node):
    def is_balance(self):
        ''' test if a node is balance in AVL rule '''
        return abs(self.delta()) <= 1

    def delta(self):
        ''' delta height between left and right branch '''
        left = self.leftChild.height if self.leftChild else 0
        right = self.rightChild.height if self.rightChild else 0
        return left - right


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
                assert node.is_balance(), \
                    '%s height delta more than 1' % node.as_tree()

                check_node(node.leftChild)
                check_node(node.rightChild)

            check_node(self.rootNode)
            return True
        except AssertionError as e:
            print str(e)
            return False

    def fixup(self, node):
        if node.parent and node.parent.parent:
            N = node
            P = node.parent
            G = P.parent
            branch = lambda p, c: 'left' if p.leftChild == c else 'right'
            if not G.is_balance():
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

                # Note here we add a condition that P.delta() != 0
                # This is because when P's children b & N has the same height,
                # rotation would make things worse.
                # (in deletion fixup, we meet this problem)
                #        3(P)                    5
                #       / \                     / \
                #   (b)2   5(N)    ---->       3   6
                #     /     \                 /
                #    1       6               2
                #                           /
                #                          1
                # more generally, if h(b) = m ,h(N) = n, h(d) = n - 1, h(P) = m + 1
                # after rotation (as graph(1)):
                # h(N) = h(P) + 1 = h(b) + 2 = m + 2
                # delta(N) = h(d) - h(P) = n - 1 - (m + 1) = n - m + 2
                # if m = n, delta(N) = 2, N break the AVL rule
                # that is to say, subtree has violate the rule, not any way
                # recursive moving upward.
                # ** for the relation between m and n.
                # 1. in insert ops, N is always the one who has one extra
                # child, so n > m
                # 2. in deletion ops, we might meet P has two child with the
                # same height, since N is found out by unbalance_leaf(), there
                # is possiblity to choose right branch till leaf in P, whereas
                # left branch is another choice.
                if P.delta() != 0 and branch(G, P) != branch(P, N):
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
        node = node_or_key if isinstance(node_or_key, Node) else ANode(node_or_key)
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
        def delete_node(node):
            ''' delete the node from tree,
            return the deleted node's parent and its original height
            '''
            # most copy from Tree.delete_node()
            if (not node.rightChild) or (not node.leftChild):
                parent = node.parent
                height = parent.height if parent else 0
                child = node.rightChild if node.rightChild else node.leftChild
                self.replace(node, child)
            else:
                successor = self.successor(node.key)
                parent = successor.parent
                height = parent.height
                self.replace(successor, successor.rightChild)
                node.key, successor.key = successor.key, node.key
            return (parent, height)

        node = self.find(key)
        if node:
            P, h_old = delete_node(node)

            # P is the parent of the deleted node.
            if not P:  # reach the rootNode, return
                # since node N to be deleted has only two possibility.
                # 1. N is the leaf
                # 2. N has only child
                # if N.parent is None, that is to say N is rootNode, in case 1,
                # after deletion, tree is emtpy. case 2, N's child become the
                # new rootNode, as a subtree, it is already meet the rules.
                return

            def unbalance_leaf(node):
                ''' find the highest child of an unbalance node.
                if we found such node, we are in the situation like insert.
                we can call fixup to rebalance tree.
                '''
                N = node
                while not N.is_leaf():
                    if N.delta() > 0:
                        N = N.leftChild
                    else:
                        N = N.rightChild
                return N

            # we can see the deletion ops in this way: P's subtree and P's
            # as a subtree of its parent.
            # There is two case might break down the AVL rules
            if not P.is_balance():
                # case 1:
                # P's subtree is unbalance, we figure out the unbalanced leaf,
                # then things goes like insertion fixup, it would do a
                # bottom-up fixup, and no need to care about whether P's height
                # is changed, since this bottom up traverse has cover this
                # case.
                N = unbalance_leaf(P)
                self.fixup(N)
            elif h_old != P.height:
                # case 2:
                # P's subtree is balanced, whereas P's height has changed.
                # so P's subtree is OK, we need to check upward.
                while P and P.is_balance():  # find out first unbalance parent
                    P = P.parent
                # height changed does not means balance break down, since AVL
                # can bear +/-1 height delta
                if P:
                    # here, we work just as case 1.
                    N = unbalance_leaf(P)
                    self.fixup(N)
