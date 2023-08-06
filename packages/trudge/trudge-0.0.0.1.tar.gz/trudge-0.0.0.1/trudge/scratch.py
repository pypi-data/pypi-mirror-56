"""Space enumeration generator data structures.

Data structures for building generators that allow enumeration
of a state space.
"""

import doctest



'''


from itertools import combinations

def splits(n, parts):
    if parts == 1:
        yield [n]
    else:
        for i in range(n+1):
            for xs in splits(n-i, parts-1):
                yield xs+[i]

#print(list(splits(3,5)))

import sys
g = splits(3,3)
for s in g:
    print(s)
    #print(sys.getsizeof(g))
'''

## eof