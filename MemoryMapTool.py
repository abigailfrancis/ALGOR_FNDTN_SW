
class TLB:
	name = ""
	memory_type = Memory_Type.NONE
	min_size = 0
	size_in_kb = 0
	start_address = 0
	
	def __init__(self, name, memory_type, min_size, size_in_kb, start_address):
	    self.name = name
		self.memory_type = memory_type
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
	