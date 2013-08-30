from tree import Node, Tree
import random

# assign a random number in range [0, 1]
random_key = random.random


class TNode(Node):
    ''' Node in Treap

    the only diff to Node is we add a priority to each node.
    '''
    def __init__(self, key):
        super(TNode, self).__init__(key)
        self.priority = random_key()

    def __str__(self):
        return str(self.key) + "(%s)" % str(self.priority)


class Treap(Tree):
    ''' Treap

    * Beauty of Random *
    Treap actually is a combination of BST and Heap.
    First, it must obey BST property, but it might violate property rules --
    parent node must has a small priority than its child. In this situation,
    we can do a left/right rotate to fix it.

    support operations:
        search -- search a key in tree, just as BST
        insert -- insert a key in tree, need to fix priority
        delete -- delete one node from tree, just as BST:
            in case 1 & 2, just delete node won't violate priority rule.
            in case 3, we swap node with its successor, however, swap key don't
                change the priority of node, so we are the same as case 1 or 2
        merge -- merge two treap into one
        split -- split treap into two with a pivot
    '''
    def sanity(self):
        try:
            # first it must meet BST property
            assert super(Treap, self).sanity(), 'BST check fail'
            # then check priority rule

            def check_node(node):
                if not node:  # end of tree
                    return
                parent = node.parent
                if parent:
                    assert parent.priority < node.priority, \
                        'Treap %s: prio wrong %s' % (self.rootNode.as_tree(), node)
                check_node(node.leftChild)
                check_node(node.rightChild)

            check_node(self.rootNode)
            return True
        except AssertionError as e:
            print (str(e))
            return False

    def insert(self, node_or_key):
        node = node_or_key if isinstance(node_or_key, Node) else TNode(node_or_key)
        if self.rootNode and not self.find(node.key):
            # insert node just like BST way
            node = self.add_as_child(self.rootNode, node)
            # fix the priority rules, node is always leaf
            self.priority_fixup(node)
        else:
            self.rootNode = node

    def priority_fixup(self, node):
        ''' bottom-up fixup priority rule when insert or delete '''
        # go upwards until we find priority meets or reach rootNode
        while node.parent and node.priority < node.parent.priority:
            # get the rotate direction
            # if node is left child, then we rotate 'right', else otherwise
            dirt = 'right' if node.parent.leftChild == node else 'left'
            self.rotate(node.parent, dirt)
            # NOTE: if we do rotation, the node becomes parent of node.parent,
            # that is to say, node becomes new parent, so we should not do node
            # = node.parent.
        self.sanity()

    def delete(self, key):
        # delete one node from tree, just as BST:
        # in case 1 & 2, just delete node won't violate priority rule.
        # in case 3, we swap node with its successor, however, swap key don't
        # change the priority of node, so we are the same as case 1 or 2
        node = self.find(key)
        if node:
            self.delete_node(node)

    def split(self, key):
        ''' split a treap with a split KEY and return two treap one each key
        less than KEY, the other bigger than KEY '''
        node = TNode(key)
        # tricky: we insert a smallest priority node to the tree, accroidng to
        # the priority rules, this node will become rootNode of the tree. In
        # the end, tree would trasformed into two part, root->leftChild which
        # has key samller that KEY, and rightChild bigger that KEY
        node.priority = 0
        self.insert(node)

        root = self.rootNode
        return Treap(root=root.leftChild), Treap(root=root.rightChild)
