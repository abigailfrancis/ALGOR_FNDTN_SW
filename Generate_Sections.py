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
    DDR_2 = TLB("DDR 2", Access_Type.Supervisor, 0x20000000, pow_of_4(0x20000000 / KB), 0x40000000)
    DDR_3 = TLB("DDR 3", Access_Type.Supervisor, 0x10000000, pow_of_4(0x10000000 / KB), 0x60000000)
    DDR_4 = TLB("DDR 4", Access_Type.Supervisor, 0x1000000, pow_of_4(0x1000000 / KB), 0x70000000)
    DDR_5 = TLB("DDR 5", Access_Type.Supervisor, 0x200000, pow_of_4(0x200000 / KB), 0x71000000)
    DDR_6 = TLB("DDR 6", Access_Type.Supervisor, 0x40000, pow_of_4(0x40000 / KB), 0x71200000)
    
    MemoryMapTool.TLB_list = [DDR_1, DDR_2, DDR_3, DDR_4, DDR_5, DDR_6]


def Generate_Memory_Sections():

    # generate memory sections
    # keep adding until no others will fit
    temp_list_master = []
    for user_TLB in [i for i in MemoryMapTool.TLB_list if i.access_type == Access_Type.User]:
        temp_list = []
        Memory_number = 0
        size_fits = True
        while(size_fits):
            size_fits = True
            size = random.randint(1, int(user_TLB.size_in_kb * KB / 20))
            alignment = random.choice([4, 8, 16, 32, 1024, 4096])
            if len(temp_list) > 0:
                for i in range(0, len(temp_list)):
                    # sort largest to smallest
                    if temp_list[i].size < size:
                        temp_list.insert(i, Memory("Memory_Section_" + user_TLB.name.replace(" ", "_") + "_" + str(Memory_number), user_TLB.name, size, alignment, user_TLB.start_address))
                        break
                # recalculate addresses
                for i in range(0, len(temp_list)):
                    if i == 0:
                        temp_list[i].start_address = (user_TLB.start_address + (temp_list[i].alignment - 1)) & ~(temp_list[i].alignment - 1)
                    else:
                        temp_list[i].start_address = (temp_list[i-1].start_address + temp_list[i-1].size + (temp_list[i].alignment - 1)) & ~(temp_list[i].alignment - 1)
                        # check if it fits
                        if (temp_list[i].start_address + temp_list[i].size) > (user_TLB.start_address + user_TLB.size_in_kb * KB):
                            # doesn't fit, remove and stop
                            del temp_list[i:len(temp_list)]
                            size_fits = False
                            break
            else:
                temp_list.append(Memory("Memory_Section_" + user_TLB.name.replace(" ", "_") + "_" + str(Memory_number), user_TLB.name, size, alignment, user_TLB.start_address))
                
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
        write.writerows([[i.name, hex(i.min_size), hex(i.size_in_kb), hex(i.start_address)] for i in MemoryMapTool.TLB_list])
        
        
    fields = ['Name', 'TLB', 'Size', 'Alignment', 'Start Address']
    with open('generated_memory_sections_' + case + '.csv', 'w') as f:
        write = csv.writer(f)
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