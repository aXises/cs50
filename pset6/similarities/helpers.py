from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    a = " " + a
    b = " " + b
    matrix = [[(0, None) for i in range(len(b))] for j in range(len(a))]
    for i in range(1, len(a)):
        matrix[i][0] = i, Operation.DELETED
    for j in range(1, len(b)):
        matrix[0][j] = j, Operation.INSERTED
    for j in range(1, len(b)):
        for i in range(1, len(a)):
            if (b[j] == a[i]):
                matrix[i][j] = matrix[i - 1][j - 1][0], Operation.SUBSTITUTED
            else:
                delete = matrix[i - 1][j][0] + 1, Operation.DELETED
                insert = matrix[i][j - 1][0] + 1, Operation.INSERTED
                sub = matrix[i - 1][j - 1][0] + 1, Operation.SUBSTITUTED
                matrix[i][j] = min(delete, insert, sub, key=lambda x: x[0])
    return matrix