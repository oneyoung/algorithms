iparent = lambda i: int(i / 2)
ileft = lambda i: i * 2
iright = lambda i: i * 2 + 1


class Heap(object):
    def __init__(self, array=[], htype='max'):
        # self.cmp is a wrapper to compare relationship between parent and
        # child node, if True, satisfied; False othrewise.
        if htype == 'max':
            self.cmp = lambda x, y: x >= y
        else:
            self.cmp = lambda x, y: x <= y
        self.create(array)

    def sanity(self):
        ''' test heap is valid '''
        # Heap is such data struct that
        # can be a tree too, but a list can save more space
        # 1. a list that can be seen as complete binary tree, root node is [0]
        # 2. parent and child can be indexed as above
        # 3. node must >= its child (max heap), or otherwise (min heap)
        # example:
        #                    200[1]
        #                    /  \
        #                  17[2] 50[3]
        #                 /  \   /   \
        #            13[4] 3[5] 25[6] 5[7]
        #           /   \
        #         9[8]  7[9]
        heap = self.heap
        length = len(self.heap)
        i = 1
        level = 0

        def check_child(i):
            l, r = ileft(i), iright(i)
            if l < length:
                assert self.cmp(heap[i], heap[l]), '%s i:%d l:%d' % (heap, i, l)
            if r < length:
                assert self.cmp(heap[i], heap[r]), '%s i:%d r:%d' % (heap, i, r)

        while i < length:
            nnode = 2 ** level  # num of node in this tree level
            for delta in range(0, nnode):
                # traverse node in level of tree
                index = i + delta
                if index < length:  # make sure not cross boundary of list
                    check_child(index)
                else:
                    break
            # prepare for next loop
            i += nnode
            level += 1

    def heapify(self, i):
        # topdown traverse
        A = self.heap
        length = len(A)
        l, r = ileft(i), iright(i)  # left and right child index

        # find the largest element
        largest = l if l < length and not self.cmp(A[i], A[l]) else i
        largest = r if r < length and not self.cmp(A[largest], A[r]) else largest
        if largest != i:  # heap rules fix
            A[i], A[largest] = A[largest], A[i]
            self.heapify(largest)

    def create(self, array):
        ''' build heap from an array '''
        # in place build heap
        self.heap = [0] + array  # index start from 1
        # no need to traverse all nodes, since some are leaves
        stop = int(len(self.heap) / 2)
        # we use a bottom-up order to avoid too much recurse
        for i in range(stop, 0, -1):
            self.heapify(i)

    def sort(self):
        ''' heap sort '''
        length = len(self.heap)
        if length <= 1:  # empty heap
            return []
        A = self.heap
        result = []
        for i in range(length - 1, 1, -1):
            # popup the root node each time, since it's max of the heap. Every
            # time we insert this number in the result list, and put the last
            # child of heap to root, doing a heapify to maintain heap property
            # until the heap has only one element.
            A[1], A[i] = A[i], A[1]
            result.insert(0, A.pop(i))
            self.heapify(1)
        result.insert(0, A[1])  # only one child left, add to result

        return result


class PriorityQueue(Heap):
    def find_top(self):
        '''find max or min element depends on type of tree'''
        assert len(self.heap) > 1, 'empty heap'
        return self.heap[1]

    def pop_top(self):
        ''' pop max or min element depends on type of tree '''
        heap = self.heap
        end = len(heap) - 1
        assert end > 0, 'empty heap'
        # swap head and tail, this is like *heap sort*
        heap[1], heap[end] = heap[end], heap[1]
        top = heap.pop(end)
        self.heapify(1)
        return top

    def update_key(self, i, key):
        ''' update rank i element to key '''
        heap = self.heap
        assert i < len(heap), 'heap overflow'
        orig = heap[i]
        heap[i] = key
        if self.cmp(key, orig):  # go upwards
            p = iparent(i)
            # swap with parent until heap property meets or reach the top
            while i > 1 and self.cmp(heap[i], heap[p]):
                heap[i], heap[p] = heap[p], heap[i]
                i = p
                p = iparent(i)
        else:  # downwards
            self.heapify(i)

    def insert_key(self, key):
        heap = self.heap
        heap.append(key)  # append to tail
        # that means we must go upwards if necessary
        i = len(heap) - 1
        p = iparent(i)
        while i > 1 and self.cmp(heap[i], heap[p]):
            heap[i], heap[p] = heap[p], heap[i]
            i = p
            p = iparent(i)
