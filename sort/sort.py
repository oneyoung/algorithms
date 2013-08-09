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
