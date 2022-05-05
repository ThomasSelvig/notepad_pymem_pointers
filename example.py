"""
How to find pointer of address:
1. open notepad + cheat engine and generate pointermap (also save addr of where text starts)
2. repeat, saving new pointermap to a new file
3. pointerscan, compare first and second pointermap (saved_pointermap and compare_pointermap(fill out addr))
4. find pointer with least pointers to follow, with base addr looking like "notepad.exe"+0x12345...

each "offset" this scan shows is the amount of times you have to follow the pointer (with offset) to get address


"""
from pymem import Pymem


notepad = Pymem("notepad.exe")


def addr_of_pointer(offset):
	return notepad.read_ulonglong(offset)


# follow pointer twice, then add final offset
text_begin = addr_of_pointer(addr_of_pointer(notepad.base_address + 0x2c470) + 0x0) + 0x0
print(f"text starts at address 0x{text_begin:x}")

# print first 5 characters (each char is 2 bytes) types in notepad
print(notepad.read_bytes(text_begin, 10))