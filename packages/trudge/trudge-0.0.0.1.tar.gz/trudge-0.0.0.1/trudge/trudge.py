"""Space enumeration generator data structures.

Data structures for building generators that allow for
the enumeration of a discrete state space using various
strategies.
"""

import doctest

class naturals():
    """Base dimension for enumerators of natural numbers."""
    def __init__(self):
        pass

class broaden():
    """
    Strategy that involves incrementally broadening
    the subset of the space when enumerating the values.
    """

    def __init__(self, *args):
        self.dimensions = args
        self.initialized = True
        self.generator = self._stages()

    def __mul__(self, other):
        """
        Combine two strategies such that the newly built
        strategy enumerates items from the Cartesian product
        of the two spaces. Only strategies that have not
        already been queried for values can be combined.
        """
        if type(other) != type(self):
            raise TypeError('Different strategies cannot be combined')
        if not self.initialized or not other.initialized:
            raise ValueError('Can only combine initialized (i.e., unused) strategies')
        
        return broaden(*self.dimensions, *other.dimensions)

    def _splits(self, n, parts):
        """
        Generate every possible way of splitting a non-negative
        integer into the specified number of non-negative integer
        terms. 
        """
        if parts == 1:
            yield [n]
        else:
            for i in range(n+1):
                for xs in self._splits(n-i, parts-1):
                    yield tuple(xs+[i])

    def _stages(self):
        """
        Generate every possible way of splitting every possible
        non-negative integer, starting from zero and going up.
        """
        n = 0
        while True:
            for split in self._splits(n, len(self.dimensions)):
                yield split
            n += 1

    def __next__(self):
        """Initialize this strategy and generate first value."""
        self.initialized = False
        return next(self.generator)

    def reset(self):
        """Reset this strategy so it can be combined with others."""
        self.initialized = True
        self.generator = self._stages()

if __name__ == "__main__": 
    doctest.testmod()
