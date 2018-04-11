import Levenshtein

def distance(string1, string2):
    n1 = len(string1)
    n2 = len(string2)
    return _levenshtein_distance_matrix(string1, string2)[n1][n2]


def _levenshtein_distance_matrix(string1, string2):
    n1 = len(string1)
    n2 = len(string2)
    d = [[0 for x in range(n2 + 1)] for y in range(n1 + 1)]
    for i in range(n1 + 1):
        # d[i, 0] = i
        d[i][0] = i
    for j in range(n2 + 1):
        # d[0, j] = j
        d[0][j] = j
    for i in range(n1):
        for j in range(n2):
            if string1[i] == string2[j]:
                cost = 0
            else:
                cost = 1
            d[i + 1][j + 1] = min(d[i][j + 1] + 1,  # insert
                                  d[i + 1][j] + 1,  # delete
                                  d[i][j] + cost)  # replace
    return d


def editops(string1, string2):
    dist_matrix = _levenshtein_distance_matrix(string1, string2)
    i, j = (len(_levenshtein_distance_matrix(string1, string2)),) + (len(_levenshtein_distance_matrix(string1, string2)[0]),)
    i -= 1
    j -= 1
    ops = list()
    while i != -1 and j != -1:
        values = [dist_matrix[i-1][j-1], dist_matrix[i][j-1], dist_matrix[i-1][j]]
        index = values.index(min(values))

        if index == 0:
            if dist_matrix[i][j] > dist_matrix[i-1][j-1]:
                ops.insert(0, ('replace', i - 1, j - 1))
            i -= 1
            j -= 1
        elif index == 1:
            ops.insert(0, ('insert', i - 1, j - 1))
            j -= 1
        elif index == 2:
            ops.insert(0, ('delete', i - 1, i - 1))
            i -= 1
    return ops

if __name__ == "__main__":
    print(Levenshtein.distance('kutbat', 'katabat'))
    print(Levenshtein.editops('kutbat', 'katabat'))

    print(distance('kutbat', 'katabat'))
    ops = editops('kutbat', 'katabat')
    print(ops)