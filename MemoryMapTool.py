from enum import Enum

TLB_list = []
Memory_list = []

KB = 1024
MB = 1024^2
GB = 1024^3

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