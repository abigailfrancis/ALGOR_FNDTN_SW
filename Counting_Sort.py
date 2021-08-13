import csv


def CountingSortStringPrep(arr, index):

    # sort arr by element at index

    length = len(max([el[index].replace('User_TLB_DDR_', '').replace('_', '') for el in arr], key = len))
    
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    for el in arr:
        el[index] = el[index].replace('User_TLB_DDR_', '').replace('_', '').ljust(length, '*')
    
    converted_arr = []
    
    for el in arr:
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
    
    print(count)
            

# put information into list
with open('generated_memory_sections_average_case.csv', newline='') as f:
	reader = csv.reader(f)
	data = list(reader)
    
# remove blank lines and headers
data = [x for x in data if x and x[0] != 'Name']
    
converted_array = CountingSortStringPrep(data, 1)
CountingSortString(data, 1, converted_array)
