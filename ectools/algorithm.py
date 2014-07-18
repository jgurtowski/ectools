import sys

def binarySearch(inlist, cmp_func, first=0, last=None):
    '''Returns index of first item that cmp_func returns 0.
    None if can't be found
    cmp_func is < 0 if the value you are looking for is
    less than what is passed to cmp_func by this function. 
    > 0 if it is more, 0 if equal.
    '''
    last = len(inlist)-1 if not last else last
    
    if last < first:
        return None
    mid = (last + first) / 2

    d = cmp_func(inlist[mid])
    if d < 0:
        last = mid - 1
    elif d > 0:
        first = mid + 1
    else:
        return mid
    return binarySearch(inlist, cmp_func, first, last)

def expandRegion(inlist, cmp_func, start=0):
    '''Expands a region in a list based on cmp_func
    While cmp_func returns true keep adding to region
    returns a tuple (first,last) for boundaries of
    the region
    '''
    if not cmp_func(inlist[start]):
        return None

    first = start
    last = start
    
    while first > 0:
        if not cmp_func(inlist[first-1]):
            break
        first -= 1

    ll = len(inlist)
    while last < (ll-1):
        if not cmp_func(inlist[last+1]):
            break
        last += 1

    return (first,last)
    
