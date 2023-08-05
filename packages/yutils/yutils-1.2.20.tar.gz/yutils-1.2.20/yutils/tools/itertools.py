#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37


def equivilence(iterator, func):
    """
    Divides an iterator to groups, based on the function's result of every item in the iterator.
    Returns dict of lists.

    Example:
        >>> equivilence(range(10), lambda x: x % 3)
        >>>out>>> {0: [0, 3, 6, 9],
        >>>out>>>  1: [1, 4, 7],
        >>>out>>>  2: [2, 5, 8]}

    :param iterator: an iterator you wish to run on and divide into groups
    :type iterator: iterator
    :param func: a function to activate on each iterator item - its result decides the return dict's keys.
    :type func: function

    :rtype: dict of lists (lists are groups of original iterator)
    """
    return_dict = {}
    for item in iterator:
        return_dict.setdefault(func(item), []).append(item)
    return return_dict


def disperse(n, m):
    """
    Disperses a number n between m different groups.
    The sum of all groups must be smaller or equal to n.
    (Yes, the sum can be smaller - that is, a group of zeros is also an answer)

    :param n: The number to disperse between groups
    :type n: int
    :param m: The amount of groups to disperse n into
    :type m: int

    :return: All of the options of dispersion
    :rtype: list of tuples (of ints)
    """
    options = [()]
    for group in range(m):
        new_options = []
        for option in options:
            remainder = n - sum(option)
            for i in range(remainder + 1):
                new_options.append(option + (i,))
        del options
        options = new_options
    return options
