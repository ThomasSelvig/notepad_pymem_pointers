# TODO get amount of chars  typed
from pymem import Pymem


notepad = Pymem("notepad.exe")


def addr_of_pointer(offset):
	return notepad.read_ulonglong(offset)

def follow_pointers(base_offset, *pointer_offsets):
	addr = addr_of_pointer(notepad.base_address + base_offset)
	for offset in pointer_offsets[:-1]:
		addr = addr_of_pointer(addr + offset)
	return addr + pointer_offsets[-1]


text_begin = addr_of_pointer(addr_of_pointer(notepad.base_address + 0x2c470) + 0x0) + 0x0
# line below: bugged because im too lazy to find correct pointer
# cursor_index = follow_pointers(0x2d470, 0x358, 0x38, 0x50, 0x18)

# print first 5 characters (each char is 2 bytes) types in notepad
# print(notepad.read_bytes(text_begin, 10))

# print(f"Cursor: {notepad.read_int(cursor_index)}")
print(f"Text: {notepad.read_bytes(text_begin, 10)}")
