import random
import math


def insert_sort(array):
    l = len(array)
    for i in range(0, l):
        for j in range(i, l):
            if array[i] > array[j]:
                array.insert(i, array.pop(j))

    return array


def insert_sort2(array):
    ''' insert sort without list insert support
        cache friendly, inplace sort, but slower
    '''
    l = len(array)
    for i in xrange(0, l - 1):
        # the head ith array has been sorted
        # insert one element[i+1] into the sorted list
        j = i + 1
        for k in xrange(0, j):
            # each loop need to compare all prev sorted array, slower
            if array[k] > array[j]:
                array[k], array[j] = array[j], array[k]
    return array


def merge_sort(array):
    def merge(a1, a2):
        ''' merge two sorted list into one '''
        ret = []
        while a1 and a2:
            if a1[0] < a2[0]:
                val = a1.pop(0)
            else:
                val = a2.pop(0)
            ret.append(val)
        return ret + a1 + a2

    def recursor(a):
        length = len(a)
        if length == 1:
            return a
        else:
            return merge(recursor(a[:length / 2]), recursor(a[length / 2:]))

    return recursor(array)


def partition(array, i_left, i_right, i_pivot):
    pivot = array[i_pivot]
    # first swap pivot to right most element
    array[i_right], array[i_pivot] = array[i_pivot], array[i_right]
    i_stored = i_left
    for i in range(i_left, i_right):  # i_left <= i < i_right
        if array[i] < pivot:  # if i < pivot, move to left side
            array[i], array[i_stored] = array[i_stored], array[i]
            i_stored += 1  # once we found a match, move 1 forward
    array[i_stored], array[i_right] = array[i_right], array[i_stored]  # move back pivot
    return i_stored  # return pivot index


def quick_sort(array):
    '''
    in-place quick sort
    '''
    def quicksort(array, i_left, i_right):
        if i_left < i_right:
            i_pivot = random.randint(i_left, i_right)  # choose a random pivot
            i_pivot_new = partition(array, i_left, i_right, i_pivot)

            # recursivly sort eles smaller than pivot
            quicksort(array, i_left, i_pivot_new - 1)

            # recursivly sort eles bigger than pivot
            quicksort(array, i_pivot_new + 1, i_right)

    quicksort(array, 0, len(array) - 1)
    return array


def quick_sort2(array):
    '''
    simple quick sort version, need more mem
    '''
    if len(array) <= 1:
        return array
    return quick_sort2([lt for lt in array[1:] if lt <= array[0]]) + \
        array[0:1] + \
        quick_sort2([gt for gt in array[1:] if gt > array[0]])


def counting_sort(array):
    # init a empty aux array
    m = max(array)
    n = min(array)

    aux = [0] * (m - n + 1)
    for a in array:  # get counting map
        aux[a - n] += 1

    # generate index map of aux
    s = 0
    for i in range(len(aux)):
        s += aux[i]
        aux[i] = s

    ret = [0] * len(array)
    for a in array[::-1]:
        i = a - n
        ret[aux[i] - 1] = a
        aux[i] -= 1
    return ret


def radix_sort(array):
    def csort(array, shift, mask):
        '''
        another type of counting sort.
        picked by shift
        '''
        # init a empty aux array

        aux = [0] * (mask + 1)
        for a in array:  # get counting map
            index = (a >> shift) & mask
            aux[index] += 1

        # generate index map of aux
        s = 0
        for i in range(len(aux)):
            s += aux[i]
            aux[i] = s

        ret = [0] * len(array)
        for a in array[::-1]:  # reverse iter make sure the order
            i = (a >> shift) & mask
            ret[aux[i] - 1] = a
            aux[i] -= 1
        return ret

    r = int(math.log(len(array), 2))  # slicer
    b = int(math.ceil(math.log(max(array), 2)))  # max bits
    mask = (2 ** r) - 1
    for i in range(int(b / r) + 1):
        shift = i * r
        array = csort(array, shift, mask)
    return array


def bucket_sort(array, size=10):
    ''' bucker sort
    para:
        array -- list to be sorted
        size -- size of bucket, default is 10
    '''
    # init empty buckets
    # should not use [[]] * size, because inner [] refer to the same empty
    # list, so each insert to that list would apply to all lists
    buckets = [[] for i in range(size)]

    # here we want to build a generic bucket sort apply to any intergers, so
    # need to figure out the range of the array
    n, m = list_range(array)
    stride = int(math.ceil((m - n) / float(size)))  # need a ceil here

    # fill in the buckets
    for i in array:
        index = int((i - n) / stride)  # choose which bucket to append
        buckets[index].append(i)

    # sort elements in each bucket
    for bucket in buckets:
        insert_sort(bucket)

    # concate each buckets into one array, and return
    return sum(buckets, [])


def list_range(array):
    '''
    get the min and max of the list
    array must not be empty
    return (min, max)
    -- time T(n) = 3*(n/2)
    '''
    length = len(array)
    if length == 0:
        raise Exception
    if length % 2 == 0:
        head = array[0:2]
        m, n = head if head[0] > head[1] else head[::-1]
        start = 2
    else:
        m = n = array[0]
        start = 1

    for i in range(start, length, 2):
        x = array[i]
        y = array[i + 1]
        mi, ni = (x, y) if x > y else (y, x)
        m = mi if mi > m else m
        n = ni if ni < n else n

    return (n, m)


def randomize_select(array, n):
    '''
    find out the nth big elements in a array
    paras:
        array -- should not have same elements
        n -- index start from 1
    '''
    def func(array, i_left, i_right, nth):
        if i_left == i_right:  # only one element left
            return i_left

        i_pivot = random.randint(i_left, i_right)  # choose a random pivot
        i_pivot_new = partition(array, i_left, i_right, i_pivot)
        if i_pivot_new == nth:  # we got the right index
            return i_pivot_new
        elif i_pivot_new > nth:
            return func(array, i_left, i_pivot_new - 1, nth)
        else:
            return func(array, i_pivot_new + 1, i_right, nth)

    length = len(array)
    if length < n:
        raise Exception
    index = func(array, 0, length - 1, n - 1)

    return array[index]
