from enum import Enum

P1_TLB_list = []
P2_TLB_list = []
P1_Memory_list = []
P2_Memory_list = []

class Access_Type(Enum):
	NONE = 0
	Supervisor = 1
	User = 2


class TLB:
	name = ""
	access_type = Access_Type.NONE
	min_size = 0
	size_in_kb = 0
	start_address = 0
	
	def __init__(self, name, access_type, min_size, size_in_kb, start_address):
		self.name = name
		self.access_type = access_type
		self.min_size = min_size
		self.size_in_kb = size_in_kb
		self.start_address = start_address


class Memory:
	name = ""
	TLB = ""
	size = 0
	alignment = 0
	start_address = 0
	
	def __init__(self, name, TLB, size, alignment, start_address):
		self.name = name
		self.TLB = TLB
		self.size = size
		self.alignment = alignment
		self.start_address = start_address


if __name__ == "__main__":
	#supervisor TLBs
	DDR_1 = TLB("DDR 1", Access_Type.Supervisor, 0x40000000, 0x100000, 0x00000000)
	DDR_2 = TLB("DDR 2", Access_Type.Supervisor, 0x20000000, 0x80000, 0x40000000)
	DDR_3 = TLB("DDR 3", Access_Type.Supervisor, 0x10000000, 0x40000, 0x60000000)
	DDR_4 = TLB("DDR 4", Access_Type.Supervisor, 0x1000000, 0x4000, 0x70000000)
	DDR_5 = TLB("DDR 5", Access_Type.Supervisor, 0x200000, 0x800, 0x71000000)
	DDR_6 = TLB("DDR 6", Access_Type.Supervisor, 0x40000, 0x100, 0x71200000)
	
	P1_TLB_list = [DDR_1, DDR_2, DDR_3, DDR_4, DDR_5, DDR_6]
	P2_TLB_list = [DDR_1, DDR_2, DDR_3, DDR_4, DDR_5, DDR_6]
	
	#print([i.name for i in P1_TLB_list])
	#print([i.name for i in P2_TLB_list])