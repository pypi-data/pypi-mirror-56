def makeArrayConsecutive2(l):
    return (max(l) - min(l) - len(l) + 1);


def almostIncreasingSequence(sequence):
    droppped = False
    last = prev = min(sequence) - 1
    for elm in sequence:
        if elm <= last:
            if droppped:
                return False
            else:
                droppped = True
            if elm <= prev:
                prev = last
            elif elm >= prev:
                prev = last = elm
        else:
            prev, last = last, elm

    return True


def matrixElementsSum(matrix):
    sum=0
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            if matrix[j][i]==0:
                break
            else:
                sum+=matrix[j][i]
    return sum

def allLongestStrings(m):
    l=[]
    b=max(len(x) for x in m)
    for i in range(len(m)):
        if len(m[i]) == b:
            l.append(m[i])
    return l


def commonCharacterCount(s1, s2):
    s = 0
    for i in s1:
        if i in s2:
            s2 = s2.replace(i, "", 1)
            s = s + 1
    return s

