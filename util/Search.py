from bisect import *
def find_le(a, x):
    """Find rightmost value less than or equal to x"""
    return bisect_right(a, x)-1

def find_ge(a, x):
    """Find leftmost value greater than x"""
    return bisect_left(a, x)
def parental_tree_search(root, childrenstr, conditionstr):
    """Returns parents of nodes that meed a given condition"""
    ret = []
    queue = [root]
    while queue:
        current = queue.pop()
        children = eval('current'+childrenstr)
        for child in children:
            if eval('child'+conditionstr):
                ret.append(current)
        #we know have a tree, so there are no back-edges etc, so no checking of that kind is
        #necessary
        queue += children
    return ret
