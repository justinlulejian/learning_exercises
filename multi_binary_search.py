def binary_search(mylist, item, p_start=0, p_end=None):
    start = p_start or 0
    end = p_end or len(mylist) - 1
    if p_end == 0:  # if provided a list w/ 1 element
        end = p_end
    search_counter = 0  # track number of search loops
    while start <= end:
        search_counter += 1
        midpoint = start + ((end - start) // 2)
        if mylist[midpoint] == item:
            print 'binary searched %s times' % search_counter
            return midpoint  # found index
        elif mylist[midpoint] > item:
            end = midpoint - 1  # reset end to lower half
            continue
        elif mylist[midpoint] < item:
            start = midpoint + 1  # reset start to upper half
            continue
    print 'binary searched %s times' % search_counter
    return -1


if __name__ == '__main__':
    # Find multiple targets in search_list w/ binary search.
    targets = [1, 4, 6, 8]
    search_list = [1, 2, 3, 4, 5, 6, 7]  # sorted list

    # This assumes that targets is sorted ascending and has unique elements.
    # Otherwise, would want to probably set()/sort so this is true since it
    # uses this assumption. This would incur a O(N Log N) cost with n being
    # the size of targets.
    start = 0
    end = len(search_list) - 1
    for target in targets:
        target_index = binary_search(search_list, target, start, end)
        if target_index == -1:
            print 'couldn\'t find target %s' % target
        elif target_index == 0:
            print 'found target %s at %s' % (target, target_index)
            start = target_index + 1
        elif target_index:
            print 'found target %s at %s' % (target, target_index)
            start = target_index + 1