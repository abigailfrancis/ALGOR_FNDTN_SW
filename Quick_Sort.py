def Quick_Sort(list_a, low, high):
    if low >= 0 and high >= 0:
        #if the indexes are in correct order, continue
        if low < high:
            #find the index of the pivot
            p = partition(list_a, low, high)
            #apply quicksort for the left side
            Quick_Sort(list_a, low, p-1)
            #apply quicksort for the right side
            Quick_Sort(list_a, p+1, high)
            
def partition(list_a, low, high):
    #set pivot value to final value of list
    pivot = list_a[high]
    #set pivot index to start of list
    i = low - 1
    for j in range(low, high):
        if list_a[j] < pivot:
            i = i + 1
            list_a[i], list_a[j] = list_a[j], list_a[i]

    list_a[i+1], list_a[high] = list_a[high], list_a[i+1]
    return i+1