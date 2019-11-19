import functools
import operator

#from https://bugs.python.org/file17343/factorial.py

product = functools.partial(functools.reduce, operator.mul)
def factorial(n):
    """Implementation of Binary-Split Factorial algorithm

    See http://www.luschny.de/math/factorial/binarysplitfact.html

    >>> f = 1
    >>> for n in range(1, 1001):
    ...     f *= n
    ...     assert(factorial(n) == f)
    """
    if n < 3:
        return [1, 1, 2][n]
    _, r = loop(n)
    return r << (n - count_bits(n))

def loop_iter(n):
    p = r = 1
    s = n.bit_length() - 2
    i = s - 1 + (n >> s & 1)
    while i >= 0:
        m = n >> i
        p *= partial_product((m >> 2) + (m >> 1 & 1), 
                             (m >> 1) + (m & 1))
        r *= p
        i -= 1
    return p, r

def loop(n):
    p = r = 1
    if n > 2:
        p, r = loop(n >> 1)
        p *= partial_product((n >> 2) + (n >> 1 & 1), 
                             (n >> 1) + (n & 1))
        r *= p
    assert(n < 3 or (p, r) == loop_iter(n)) 
    return p, r

def partial_product(start, stop):
    length = stop - start
    if length == 1:
        return start << 1 | 1
    if length == 2:
        x = (start << 1 | 1)
        return x * (x + 2)
    middle = start + (length >> 1) 
    return partial_product(start, middle) * partial_product(middle, stop)

def count_bits(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count

import sys

if sys.argv[1] == 'bench':
    factorial(int(sys.argv[2]))




