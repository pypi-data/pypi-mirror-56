#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def get_suffixes(length):
    """Create a list of suffixes to be able to merge all files after."""
    import itertools
    import math
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    r = int(math.ceil(length/len(alpha)))
    product = list(itertools.product(alpha, repeat=r))[:length]
    return sorted(["".join(x) for x in product])
