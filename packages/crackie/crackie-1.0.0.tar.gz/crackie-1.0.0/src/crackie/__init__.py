# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
from array import array
from functools import reduce

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound

def each_possible_combination(components):
    """Generator for all the combinations described in the passed list.

    Provide a list of lists, and the generator will yield a tuple for each
    possible combination of one element from the first list, one from the
    second, etc.

    Examples:

    >>> from crackie import each_possible_combination
    >>> [c for c in each_possible_combination([['a']])]
    [('a',)]
    >>> [c for c in each_possible_combination([{'a'}, {'a'}])]
    [('a', 'a')]
    >>> [c for c in each_possible_combination([('a', 'b')])]
    [('a',), ('b',)]
    >>> [c for c in each_possible_combination((('H', 'h'), ('I', 'i', '1')))]
    [('H', 'I'), ('h', 'I'), ('H', 'i'), ('h', 'i'), ('H', '1'), ('h', '1')]
    >>> combinations = [c for c in each_possible_combination(('Hh', 'Ee3', 'Ll1', 'Ll1', 'Oo0'))]
    >>> combinations[0]
    ('H', 'E', 'L', 'L', 'O')
    >>> combinations[-1]
    ('h', '3', '1', '1', '0')
    >>> len(combinations)
    162
    """
    components = [tuple(c) for c in components]
    lengths = [len(c) for c in components]
    for indexes in each_possible_index_tuple(lengths):
        next_index_list = [components[i][index] for i, index in enumerate(indexes)]
        yield tuple(next_index_list)


def each_possible_index_tuple(lengths):
    """Generator for all possible combinations from 0 to the given numbers.

    Provide a list of numbers [N_0, ..., N_n], and the generator will yield
    tuples of integers (C_0, ..., C_n) such that 0 <= C_x < N_x and 0 <= x < n.

    Examples:

    >>> from crackie import each_possible_index_tuple
    >>> [c for c in each_possible_index_tuple([1])]
    [(0,)]
    >>> [c for c in each_possible_index_tuple([1, 1])]
    [(0, 0)]
    >>> [c for c in each_possible_index_tuple([1, 1])]
    [(0, 0)]
    >>> [c for c in each_possible_index_tuple((2, 3))]
    [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
    >>> combinations = [c for c in each_possible_index_tuple((2, 3, 3, 3, 3))]
    >>> combinations[0]
    (0, 0, 0, 0, 0)
    >>> combinations[-1]
    (1, 2, 2, 2, 2)
    >>> len(combinations)
    162
    """
    indexes = array('I', [0 for _position in lengths])

    while True:
        yield tuple(indexes)
        for i, index in enumerate(indexes):
            next_index = index + 1
            if next_index == lengths[i]:
                indexes[i] = 0
            else:
                indexes[i] = next_index
                break

            if i + 1 == len(indexes):
                return

def count_possible_combinations(components):
    """Return the number of combinations for a given list of variations.

    This sounds fancier than it is: it's just the product of the lengths of the
    given list of lists.
    If you have a list that can be used with ``each_possible_combination()``, this
    function will tell you how many possible combinations there are for that list.

    Examples:

    >>> from crackie import count_possible_combinations
    >>> count_possible_combinations([['a']])
    1
    >>> count_possible_combinations([['a'], ['a']])
    1
    >>> count_possible_combinations([{'a', 'b'}])
    2
    >>> count_possible_combinations(({'H', 'h'}, {'E', 'e', '3'}, {'Y', 'y'}))
    12
    >>> count_possible_combinations(('Hh', 'Ee3', 'Ll1', 'Ll1', 'Oo0'))
    162
    """
    return reduce(
        (lambda acc, component: acc * len(component)),
        components,
        1
    )
