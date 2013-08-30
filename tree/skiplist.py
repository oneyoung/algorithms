import random


class SkipNode(object):
    def __init__(self, key):
        self.key = key
        self.prev = None
        self.next = None
        self.child = None
        self.height = 0

    def __repr__(self):
        return '%s[%s]' % (self.key, self.height)

    def insert(self, prev):
        ''' insert a node after prev '''
        self.height = prev.height
        self.prev, self.next = prev, prev.next
        n = prev.next
        prev.next = self
        if n:  # in case end of list
            n.prev = self

    def detach(self):
        self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        self.prev, self.next = None, None
        self.child = None

    def add_child(self, child):
        self.child = child


class SkipList(object):
    '''SKipList

    example:
                            45                   -- l3
                            |
          14----------------45-------------99    -- l2
          |                 |              |
    10----14----------33----45----89-------99    -- l1
    |     |           |     |     |        |
    10-13-14-18-19-20-33-41-45-56-89-90-95-99    -- l0
    '''
    def __init__(self, keys=[]):
        self.heads = []
        for k in keys:
            self.insert(k)

    def insert(self, key):
        def new_layer():
            # in each layer, we init with two -inf & inf node
            head = SkipNode(float('-inf'))
            head.height = len(self.heads)
            SkipNode(float('inf')).insert(head)
            self.heads.append(head)
            if head.height:
                # if not base layer, we should update head's child in order to
                # be reference by find ops
                head.child = self.heads[head.height - 1]

        def insert_to_layer(node, height):
            if len(self.heads) <= height:
                new_layer()
            prev = self.heads[height]
            while prev.key < node.key:
                prev = prev.next
            # now prev is the first node with key equal or bigger than node.key
            # so we just insert node before prev.prev should meet the demand
            node.insert(prev.prev)
            return node

        node = SkipNode(key)
        insert_to_layer(node, 0)
        child = node
        while random.randint(0, 1):
            parent = SkipNode(key)
            parent.add_child(child)  # track child node
            child = insert_to_layer(parent, child.height + 1)

    def find(self, key):
        ''' find a key in SkipList '''
        if not len(self.heads):  # empty list
            return None
        node = self.heads[-1]
        while node:
            # find a node until node has a equal or bigger key
            while node and node.key < key:
                node = node.next
            if node.key == key:
                # since we has a copy of key in each level, so no matter we
                # found a match key, just return the first match node
                break
            else:
                # traverse to next level
                node = node.prev.child
        return node

    def delete(self, key):
        ''' delete a node with KEY '''
        node = self.find(key)
        # once we found a valid node, we can delete up-down through child
        # pointer until bottom
        while node:
            child = node.child
            height = node.height
            node.detach()
            # check current layer, if there is not node found, we just remove
            # that layer
            head = self.heads[height]
            if not head.next.next:  # only two node left, no valid node
                self.heads.pop(height)
            node = child

    def get_layer(self, height):
        node = self.heads[height]
        result = []
        while node:
            result.append(node)
            node = node.next
        return result[1:-1]

    def as_list(self):
        if len(self.heads):
            return self.get_layer(0)
        else:
            return []

    def __str__(self):
        return '\n'.join([str(self.get_layer(h))
                          for h in range(len(self.heads))])
