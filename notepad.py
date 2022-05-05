# TODO get amount of chars  typed
from pymem import Pymem
import win32api, win32con, win32gui


notepad = Pymem("notepad.exe")


def addr_of_pointer(offset):
	return notepad.read_ulonglong(offset)

def follow_pointers(base_offset, *pointer_offsets):
	addr = addr_of_pointer(notepad.base_address + base_offset)
	for offset in pointer_offsets[:-1]:
		addr = addr_of_pointer(addr + offset)
	return addr + pointer_offsets[-1]


# text_begin = addr_of_pointer(addr_of_pointer(notepad.base_address + 0x2c470) + 0x0) + 0x0
text_addr = follow_pointers(0x2c470, 0, 0)
# print first 5 characters (each char is 2 bytes) types in notepad
# print(f"Text: {notepad.read_bytes(text_addr, 20)}")

# 0x2cec8 is green address, meaning it's static without being a pointer
# cursor pos (from top left)
x = notepad.read_long(notepad.base_address + 0x2cec8)
y = notepad.read_long(notepad.base_address + 0x2cecc)

length_addr = follow_pointers(0x2b240, 0x188, 0x60, 0xe0, 0x298, 0xc38)

def get_text(text_addr, length_addr):
	length = notepad.read_long(length_addr)
	# text = notepad.read_bytes(text_addr, length * 2)
	text = "".join([notepad.read_char(text_addr + i * 2) for i in range(length)])
	return text

# print(get_text(text_addr, length_addr))

def set_text(string, text_addr, length_addr):
	# add b"\x00" padding after every char
	byte_repr = b""
	for i in bytes(string, "utf8"):
		byte = bytes(chr(i), "utf8")
		byte_repr += byte + b"\x00"
	
	# write length of text to render
	notepad.write_long(length_addr, len(string))
	# write text
	notepad.write_bytes(text_addr, byte_repr, len(byte_repr))

# set_text("hei\r\nog\r\nhallo", text_addr, length_addr)
print(get_text(text_addr, length_addr))
print(f"Text: {notepad.read_bytes(text_addr, 20)}")

# redraw window
hwnd = win32gui.FindWindow(None, "*Untitled - Notepad")
win32gui.InvalidateRect(hwnd, None, True)
win32gui.UpdateWindow(hwnd)



# line below: bugged because im too lazy to find correct pointer
# cursor_index = follow_pointers(0x2d470, 0x358, 0x38, 0x50, 0x18)
# print(f"Cursor: {notepad.read_int(cursor_index)}")



