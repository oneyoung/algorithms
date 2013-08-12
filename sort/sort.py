import random
import math


def insert_sort(array):
    l = len(array)
    for i in range(0, l):
        for j in range(i, l):
            if array[i] > array[j]:
                array.insert(i, array.pop(j))

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


def quick_sort(array):
    '''
    in-place quick sort
    '''
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
    return quick_sort2([lt for lt in array[1:] if lt < array[0]]) + \
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
