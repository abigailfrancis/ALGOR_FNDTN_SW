import pandas as pd
import math
import Generate_Sections
import Quick_Sort
import time
#Generate_Sections.Generate_Sections()

memory = pd.read_csv('generated_memory_sections_best_case.csv')

start_time = time.perf_counter()
memory1 = memory.sort_values(by='Alignment', ascending=False, kind='mergesort')
end_time = time.perf_counter()
print("--- %s seconds ---" % (end_time - start_time))
start_time = time.perf_counter()
memory2 = memory.sort_values(by='Alignment', ascending=False, kind='quicksort')
end_time = time.perf_counter()
print("--- %s seconds ---" % (end_time - start_time))

Alignment_DF = [[], [], [], [], [], []]

for index, row in memory.iterrows():
    Alignment_DF[int(math.log(int(str(row['Alignment']), 16), 4)) - 1].append(row)
    
