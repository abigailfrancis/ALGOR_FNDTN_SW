import MemoryMapTool
from MemoryMapTool import KB, TLB, Memory, Access_Type
import random
import math
from copy import deepcopy
import csv

def pow_of_4(n):
    return int(4 ** math.ceil(math.log(n, 4)))

   
def main():
    
    #supervisor TLBs
    DDR_1 = TLB("DDR 1", Access_Type.Supervisor, 0x40000000, pow_of_4(0x40000000 / KB), 0x00000000)
    DDR_2 = TLB("DDR 2", Access_Type.Supervisor, 0x10000000, pow_of_4(0x10000000 / KB), DDR_1.start_address + DDR_1.size_in_kb * KB)
    DDR_3 = TLB("DDR 3", Access_Type.Supervisor, 0x4000000, pow_of_4(0x4000000 / KB), DDR_2.start_address + DDR_2.size_in_kb * KB)
    DDR_4 = TLB("DDR 4", Access_Type.Supervisor, 0x1000000, pow_of_4(0x1000000 / KB), DDR_3.start_address + DDR_3.size_in_kb * KB)
    DDR_5 = TLB("DDR 5", Access_Type.Supervisor, 0x100000, pow_of_4(0x100000 / KB), DDR_4.start_address + DDR_4.size_in_kb * KB)
    DDR_6 = TLB("DDR 6", Access_Type.Supervisor, 0x40000, pow_of_4(0x40000 / KB), DDR_5.start_address + DDR_5.size_in_kb * KB)
    
    MemoryMapTool.TLB_list = [DDR_1, DDR_2, DDR_3, DDR_4, DDR_5, DDR_6]

    
def compile_list(user_TLB, Memory_number, temp_list_alignments):
    size = random.randint(1, int(user_TLB.size_in_kb * KB / 20))
    alignment = random.choice([4, 16, 64, 256, 1024, 4096]) # powers of 4 from 4 to 4096
    temp_list_alignments[int(math.log(alignment, 4)) - 1].append(Memory("Memory_Section_" + user_TLB.name.replace(" ", "_") + "_" + str(Memory_number), user_TLB.name, size, alignment, user_TLB.start_address))
    # sort in descending order
    for sections in temp_list_alignments:
        sections.sort(key=lambda x: x.size, reverse=True)
    # put biggest alignments first
    temp_list = deepcopy(temp_list_alignments[len(temp_list_alignments)-1])
    # calculate addresses
    for i in range(0, len(temp_list)):
        if i == 0:
            temp_list[i].start_address = user_TLB.start_address + (temp_list[i].alignment - 1) & ~(temp_list[i].alignment - 1)
        else:
            temp_list[i].start_address = temp_list[i-1].start_address + temp_list[i-1].size + (temp_list[i].alignment - 1) & ~(temp_list[i].alignment - 1)
    for sections in [ele for ele in reversed(temp_list_alignments[:-1])]:
        for section in sections:
            inserted = False
            for i in range(0, len(temp_list)-1):
                if (((temp_list[i].start_address + temp_list[i].size + (section.alignment - 1)) & ~(section.alignment - 1)) + section.size) <= temp_list[i+1].start_address:
                    section.start_address = temp_list[i].start_address + temp_list[i].size + (section.alignment - 1) & ~(section.alignment - 1)
                    temp_list.insert(i+1, section)
                    inserted = True
                    break
            if inserted == False:
                if len(temp_list) == 0:
                    section.start_address = user_TLB.start_address + (section.alignment - 1) & ~(section.alignment - 1)
                    temp_list.append(section)
                else:
                    section.start_address = temp_list[len(temp_list)-1].start_address + temp_list[len(temp_list)-1].size + (section.alignment - 1) & ~(section.alignment - 1)
                    if section.start_address > (user_TLB.start_address + user_TLB.size_in_kb * KB):
                        return False, temp_list
                    temp_list.append(section)
                    
    return True, temp_list


def Generate_Memory_Sections():

    # generate memory sections
    # keep adding until no others will fit
    temp_list_master = []
    for user_TLB in [i for i in MemoryMapTool.TLB_list if i.access_type == Access_Type.User]:
        temp_list = []
        Memory_number = 0
        size_fits = True
        temp_list_alignments = [[],[],[],[],[],[]]
        while(size_fits):
            size_fits, temp_list = compile_list(user_TLB, Memory_number, temp_list_alignments)
                
            Memory_number = Memory_number + 1
            
            if size_fits == False:
                temp_list_master.extend(temp_list)
                
    MemoryMapTool.Memory_list.extend(temp_list_master)

   
def Generate_TLBs():

    # generate user TLBs
    # keep adding until no others will fit
    temp_list_master = []
    for supervisor_TLB in MemoryMapTool.TLB_list:
        temp_list = []
        TLB_number = 0
        size_fits = True
        while(size_fits):
            size_fits = True
            size = random.randint(1, supervisor_TLB.size_in_kb * KB / 4)
            if len(temp_list) > 0:
                for i in range(0, len(temp_list)):
                    # sort largest to smallest
                    if temp_list[i].min_size < size:
                        temp_list.insert(i, TLB("User_TLB_" + supervisor_TLB.name.replace(" ", "_") + "_" + str(TLB_number), Access_Type.User, size, pow_of_4(size/KB), supervisor_TLB.start_address))
                        break
                # recalculate addresses
                for i in range(0, len(temp_list)):
                    # first one must be aligned to its own size
                    if i == 0:
                        temp_list[i].start_address = (supervisor_TLB.start_address + (temp_list[i].size_in_kb * KB - 1)) & ~(temp_list[i].size_in_kb * KB - 1)
                    else:
                        temp_list[i].start_address = temp_list[i-1].start_address + temp_list[i-1].size_in_kb * KB
                        # check if it fits
                        if (temp_list[i].start_address + temp_list[i].size_in_kb * KB) > (supervisor_TLB.start_address + supervisor_TLB.size_in_kb * KB):
                            # doesn't fit, remove and stop
                            del temp_list[i:len(temp_list)]
                            size_fits = False
                            break
            else:
                temp_list.append(TLB("User_TLB_" + str(TLB_number), Access_Type.User, size, pow_of_4(size/KB), supervisor_TLB.start_address))
                
            TLB_number = TLB_number + 1
            
            if size_fits == False:
                temp_list_master.extend(temp_list)
                
    MemoryMapTool.TLB_list.extend(temp_list_master)


def Reverse():
    MemoryMapTool.TLB_list.sort(key=lambda x: x.start_address, reverse=True)
    MemoryMapTool.Memory_list.sort(key=lambda x: x.start_address, reverse=True)
    
def Shuffle():
    random.shuffle(MemoryMapTool.TLB_list)
    random.shuffle(MemoryMapTool.Memory_list)

    
def Create_CSV(case):
    fields = ['Name', 'Min Size', 'Size In KB', 'Start Address']
    with open('generated_tlbs_' + case + '.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows([[i.name, hex(i.min_size), hex(i.size_in_kb), hex(i.start_address)] for i in MemoryMapTool.TLB_list if i.access_type == Access_Type.User])
        
        
    fields = ['Name', 'TLB', 'Size', 'Alignment', 'Start Address']
    with open('generated_memory_sections_' + case + '.csv', 'w') as g:
        write = csv.writer(g)
        write.writerow(fields)
        write.writerows([[i.name, i.TLB, hex(i.size), hex(i.alignment), hex(i.start_address)] for i in MemoryMapTool.Memory_list])


if __name__ == "__main__":
    main()
    Generate_TLBs()
    Generate_Memory_Sections()
    Create_CSV('best_case')
    Reverse()
    Create_CSV('worst_case')
    Shuffle()
    Create_CSV('average_case')