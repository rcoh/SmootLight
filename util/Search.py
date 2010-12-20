from bisect import *
def find_le(a, x):
    'Find rightmost value less than or equal to x'
    return bisect_right(a, x)-1

def find_ge(a, x):
    'Find leftmost value greater than x'
    return bisect_left(a, x)
