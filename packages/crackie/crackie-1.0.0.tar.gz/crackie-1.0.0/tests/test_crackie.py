# -*- coding: utf-8 -*-

import pytest
import crackie

__author__ = "Pablo Brasero Moreno"
__copyright__ = "Pablo Brasero Moreno"
__license__ = "mit"

def test_each_possible_combination():
    components = [{'a', 'A', 'aa'}, {'x'}, {'2', 'two'}]
    combinations = [x for x in crackie.each_possible_combination(components)]
    assert ('a',  'x', '2')   in combinations
    assert ('a',  'x', 'two') in combinations
    assert ('A',  'x', '2')   in combinations
    assert ('A',  'x', 'two') in combinations
    assert ('aa', 'x', '2')   in combinations
    assert ('aa', 'x', 'two') in combinations

def test_each_possible_index_tuple():
    lengths = [3, 2, 3, 1]
    combinations = [x for x in crackie.each_possible_index_tuple(lengths)]

    assert (0, 0, 0, 0) in combinations
    assert (0, 0, 1, 0) in combinations
    assert (0, 0, 2, 0) in combinations
    assert (0, 1, 0, 0) in combinations
    assert (0, 1, 1, 0) in combinations
    assert (0, 1, 2, 0) in combinations
    assert (1, 0, 0, 0) in combinations
    assert (1, 0, 1, 0) in combinations
    assert (1, 0, 2, 0) in combinations
    assert (1, 1, 0, 0) in combinations
    assert (1, 1, 1, 0) in combinations
    assert (1, 1, 2, 0) in combinations
    assert (2, 0, 0, 0) in combinations
    assert (2, 0, 1, 0) in combinations
    assert (2, 0, 2, 0) in combinations
    assert (2, 1, 0, 0) in combinations
    assert (2, 1, 1, 0) in combinations
    assert (2, 1, 2, 0) in combinations

def test_count_possible_combinations():
    components = [{'a', 'A', 'aa'}, {'x'}, {'2', 'two'}]
    assert crackie.count_possible_combinations(components) == 6

    components = [{'a', 'A', 'aa'}, {'x', 'X'}, {'2', 'two'}, {'0', '1', '2', '3'}]
    assert crackie.count_possible_combinations(components) == 48
