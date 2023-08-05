def makeArrayConsecutive2(statues):
    ln = len(statues)
    print('len:' + str(ln))
    first = min(statues)
    print('first:' + str(first))
    last = max(statues)
    print('last:' + str(last))
    diff = last - first
    print('diff:' + str(diff))
    return diff - ln + 1


def first_bad_pair(sequence, k):
    """Return the first index of a pair of elements in sequence[]
    for indices k-1, k+1, k+2, k+3, ... where the earlier element is
    not less than the later element. If no such pair exists, return -1."""
    if 0 < k < len(sequence) - 1:
        if sequence[k - 1] >= sequence[k + 1]:
            return k - 1
    for i in range(k + 1, len(sequence) - 1):
        if sequence[i] >= sequence[i + 1]:
            return i
    return -1


def almostIncreasingSequence(sequence):
    """Return whether it is possible to obtain a strictly increasing
    sequence by removing no more than one element from the array."""
    j = first_bad_pair(sequence, -1)
    if j == -1:
        return True
    if first_bad_pair(sequence, j) == -1:
        return True
    if first_bad_pair(sequence, j + 1) == -1:
        return True
    return False


def matrixElementsSum(matrix):
    cost = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] != 0:
                print('adding: ' + str(matrix[i][j]))
                cost += matrix[i][j]
            else:
                print('zeroing from : ' + str(i) + str(j))
                for item in matrix:
                    item[j] = 0
    return cost


def allLongestStrings(inputArray):
    ln = 0
    for i in inputArray:
        if len(i) > ln:
            ln = len(i)
    lt = []
    for i in inputArray:
        if len(i) == ln:
            lt.append(i)
    return lt


def commonCharacterCount(s1, s2):
    s1 = list(s1)
    s2 = list(s2)
    count = 0
    print('set(s1):' + str(set(s1)))
    for i in set(s1):
        while (i in s1) and (i in s2):
            count += 1

            s1.remove(i)
            s2.remove(i)
    return count
