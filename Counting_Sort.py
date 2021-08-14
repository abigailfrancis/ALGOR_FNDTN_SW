import csv
from copy import deepcopy
import math
import sys, threading

def CountingSortStringPrep(arr, index):

    # sort arr by element at index
    
    arr_copy = deepcopy(arr)

    length = len(max([el[index].replace('User_TLB_DDR_', '').replace('_', '') for el in arr_copy], key = len))
    
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    for el in arr_copy:
        el[index] = el[index].replace('User_TLB_DDR_', '').replace('_', '').ljust(length, '*')
    
    converted_arr = []
    
    for el in arr_copy:
        converted_data = [characters.index(i.lower()) for i in el[index]]
        converted_arr.append(converted_data)

    return converted_arr
    
    
def CountingSortString(arr, index, converted_arr):
    
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    # length should always be 2
    count = [[0]*len(characters) for i in range(len(characters))]

    for x in converted_arr:
        count[x[0]][x[1]] += 1
        
    for x in range(len(count)):
        for y in range(len(count)):
            if x == 0 and y == 0:
                continue
            if y == 0:
               count[x][y] = count[x-1][9] + count[x][y]
            else:
                count[x][y] = count[x][y-1] + count[x][y]
    
    sorted_arr = [None for i in range(len(arr))]

    # determine position in sorted array
    for x in range(len(converted_arr)):   
        sorted_arr[len(converted_arr) - count[converted_arr[x][0]][converted_arr[x][1]]] = deepcopy(arr[x])
        count[converted_arr[x][0]][converted_arr[x][1]] -= 1
    
    arr = sorted_arr
    
    return arr

def CountingSort(arr, index):

    arr_copy = deepcopy(arr)
    
    max_in = max([int("0x"+el[index], 16) for el in arr_copy])
    min_in = min([int("0x"+el[index], 16) for el in arr_copy])
    
    arr_copy = [[int("0x"+x, 16) if i == index else x for i,x in enumerate(y)] for y in arr_copy]
    
    output = [None for i in range(len(arr))]
    
    count = [0 for i in range(max_in+1)]
    
    for i in arr_copy:
        count[i[index]] += 1
        
    for i in range(min_in, len(count)):
        if i != 0:
            count[i] += count[i-1]
        
    for i in range(len(arr_copy)):
        output[count[arr_copy[i][index]]-1] = deepcopy(arr[i])
        count[arr_copy[i][index]] -= 1
            
    arr = output[::-1]
    
    return arr, max_in-min_in
    
def MergeSort(arr, index):

    if len(arr) > 1:
    
        mid = len(arr)//2
        
        L = arr[:mid]
        
        R = arr[mid:]
        
        MergeSort(L, index)
        
        MergeSort(R, index)
        
        i = j = k = 0
        
        while i < len(L) and j < len(R):
            if int("0x"+L[i][index],16) > int("0x"+R[j][index],16):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            
def MergeSortString(arr, index):

    if len(arr) > 1:
    
        mid = len(arr)//2
        
        L = arr[:mid]
        
        R = arr[mid:]
        
        MergeSortString(L, index)
        
        MergeSortString(R, index)
        
        i = j = k = 0
        
        while i < len(L) and j < len(R):
            if max(L[i][index].lower(), R[j][index].lower()) == L[i][index].lower():
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    
def Buckets(arr):

    x = 0
    buckets_tlb = []
    
    # put TLBs in buckets
    for i in range(len(arr)):
        if i == 0: 
            buckets_tlb.append([])
            buckets_tlb[x].append(arr[i])
        elif arr[i-1][1] != arr[i][1]:
            buckets_tlb.append([])
            x += 1
            buckets_tlb[x].append(arr[i])
        else:
            buckets_tlb[x].append(arr[i])
    
    buckets_align = []
    
    # put alignment into buckets
    for i in range(len(buckets_tlb)):
        buckets_align.append([[],[],[],[],[],[]])
        for j in range(len(buckets_tlb[i])):
            buckets_align[i][6 - int(math.log(int("0x"+buckets_tlb[i][j][3], 16), 4))].append(buckets_tlb[i][j])
    
    return buckets_align
    
    
def Buckets_Merge(arr):

    x = 0
    buckets_tlb = []
    
    # put TLBs in buckets
    for i in range(len(arr)):
        if i == 0: 
            buckets_tlb.append([])
            buckets_tlb[x].append(arr[i])
        elif arr[i-1][1] != arr[i][1]:
            buckets_tlb.append([])
            x += 1
            buckets_tlb[x].append(arr[i])
        else:
            buckets_tlb[x].append(arr[i])
    
    buckets_align = []
    
    # put alignment into buckets
    for i in range(len(buckets_tlb)):
        buckets_align.append([[],[],[],[],[],[]])
        for j in range(len(buckets_tlb[i])):
            buckets_align[i][6 - int(math.log(int("0x"+buckets_tlb[i][j][3], 16), 4))].append(buckets_tlb[i][j])
            
    for TLB in range(len(buckets_align)):
        for alignment in range(len(buckets_align[TLB])):
            MergeSort(buckets_align[TLB][alignment], 2)
    
    return buckets_align

    
def address_calculation(arr, TLB_arr):

    temp_list_finished = []
    
    # index 4 = start address
    # index 3 = alignment
    # index 2 = size
    # index 1 = name of TLB

    for TLB in arr:
        # place biggest addresses first
        temp_list = deepcopy(TLB[0])
        for i in range(len(temp_list)):
            if i == 0:
                temp_list[i][4] = hex(int("0x"+next((x[3] for x in TLB_arr if x[0] == temp_list[i][1])),16) + (int("0x"+temp_list[i][3],16) - 1) & ~(int("0x"+temp_list[i][3],16) - 1)).replace("0x","")
            else:
                temp_list[i][4] = hex(int("0x"+temp_list[i-1][4],16) + int("0x"+temp_list[i-1][2],16) + (int("0x"+temp_list[i][3],16) - 1) & ~(int("0x"+temp_list[i][3],16) - 1)).replace("0x","")
        for alignment in TLB[1:]:
            for section in alignment:
                inserted = False
                for i in range(len(temp_list)-1):
                    if (((int("0x"+temp_list[i][4],16) + int("0x"+temp_list[i][2],16) + (int("0x"+section[3],16) - 1)) & ~(int("0x"+section[3],16) - 1)) + int("0x"+section[2],16)) <= int("0x"+temp_list[i+1][4],16):
                        section[4] = hex(int("0x"+temp_list[i][4],16) + int("0x"+temp_list[i][2],16) + (int("0x"+section[3],16) - 1) & ~(int("0x"+section[3],16) - 1)).replace("0x","")
                        temp_list.insert(i+1, section)
                        inserted = True
                        break
                if inserted == False:
                    if len(temp_list) == 0:
                        section[4] = hex(int("0x"+next((x[3] for x in TLB_arr if x[0] == section[1])),16) + (int("0x"+section[3],16) - 1) & ~(int("0x"+section[3],16) - 1)).replace("0x","")
                        temp_list.append(section)
                    else:
                        section[4] = hex(int("0x"+temp_list[len(temp_list)-1][4],16) + int("0x"+temp_list[len(temp_list)-1][2],16) + (int("0x"+section[3],16) - 1) & ~(int("0x"+section[3],16) - 1)).replace("0x","")
                        temp_list.append(section)
                   
        temp_list_finished.extend(temp_list)
        
    return temp_list_finished
                

def counting_sort_addresses():
    # put information into list
    with open('generated_memory_sections_average_case.csv', newline='') as f:
        reader = csv.reader(f)
        memory_data = list(reader)
        
    with open('generated_tlbs_average_case.csv', newline='') as g:
        reader = csv.reader(g)
        TLB_data = list(reader)
        
    # remove blank lines and headers
    memory_data = [x for x in memory_data if x and x[0] != 'Name']

    TLB_data = [x for x in TLB_data if x and x[0] != 'Name']

    # then sort by size
    # O(n + k)
    memory_data, k = CountingSort(memory_data, 2)

    # then sort by alignment
    # O(n + k)
    memory_data, k = CountingSort(memory_data, 3)

    # sort by TLB last
    # O(n + 10)
    converted_array = CountingSortStringPrep(memory_data, 1)
    memory_data = CountingSortString(memory_data, 1, converted_array)

    # put into buckets by TLB
    buckets = Buckets(memory_data)

    # calculate addresses
    finished_memory = address_calculation(buckets, TLB_data)

    # sort ascending - cant use counting sort because too much data
    finished_memory = sorted(finished_memory, key = lambda x: int("0x"+x[4],16))

    
def merge_sort_addresses():
    # put information into list
    with open('generated_memory_sections_average_case.csv', newline='') as f:
        reader = csv.reader(f)
        memory_data = list(reader)
        
    with open('generated_tlbs_average_case.csv', newline='') as g:
        reader = csv.reader(g)
        TLB_data = list(reader)
        
    # remove blank lines and headers
    memory_data = [x for x in memory_data if x and x[0] != 'Name']

    TLB_data = [x for x in TLB_data if x and x[0] != 'Name']
    
    # then sort by size
    # O(n log n)
    #MergeSort(memory_data, 2)

    # then sort by alignment
    # O(n log n)
    MergeSort(memory_data, 3)

    # sort by TLB last
    # O(n log n)
    MergeSortString(memory_data, 1)

    # put into buckets by TLB
    buckets = Buckets_Merge(memory_data)

    # calculate addresses
    finished_memory = address_calculation(buckets, TLB_data)

    # sort ascending
    finished_memory = sorted(finished_memory, key = lambda x: int("0x"+x[4],16))
    
def python_sort_addresses():
    # put information into list
    with open('generated_memory_sections_average_case.csv', newline='') as f:
        reader = csv.reader(f)
        memory_data = list(reader)
        
    with open('generated_tlbs_average_case.csv', newline='') as g:
        reader = csv.reader(g)
        TLB_data = list(reader)
        
    # remove blank lines and headers
    memory_data = [x for x in memory_data if x and x[0] != 'Name']

    TLB_data = [x for x in TLB_data if x and x[0] != 'Name']
    
    # then sort by size
    # O(n log n)
    memory_data = sorted(memory_data, key = lambda x: int("0x"+x[2],16), reverse=True)

    # then sort by alignment
    # O(n log n)
    memory_data = sorted(memory_data, key = lambda x: int("0x"+x[3],16), reverse=True)

    # sort by TLB last
    # O(n log n)
    memory_data = sorted(memory_data, key = lambda x: x[1].lower(), reverse=True)

    # put into buckets by TLB
    buckets = Buckets(memory_data)

    # calculate addresses
    finished_memory = address_calculation(buckets, TLB_data)

    # sort ascending
    finished_memory = sorted(finished_memory, key = lambda x: int("0x"+x[4],16))
    
counting_sort_addresses()
merge_sort_addresses()
python_sort_addresses()