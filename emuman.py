#! /usr/bin/python
# File: emuman.py

from tkinter import *
import filereader
import os
from os.path import isfile, join

##
#			  #
#	Variables #
#			  #
##

rompath = ""
emupath = ""
rom = ""


##
#						  #
#	Function Declarations #
#						  #
##

def run_game() :
	
	global root
	global f_reader
	global listbox
	global listbox2
	global rompath
	global emupath
	global rom
	

	
	rom = listbox2.get(ACTIVE)
	print(rom)
	
	if rom == "" or rompath == "" or emupath == "" :
		print("Error, not a valid choice")
	else : 
		root.withdraw()
		st = emupath + ' "' + rompath + rom + '"'
		#print(st)
		os.system(st)
		root.update()
		root.deiconify()
	

def updatelist(event) :
	
	global root
	global f_reader
	global listbox
	global listbox2
	global emupath
	global rompath
	
	
	index = listbox.curselection()
	print(index[0])
	emupath = f_reader.ret_path(index[0])
	rompath = f_reader.ret_rom(index[0])
	print(rompath)
	listbox2.delete(0,END)
	
	if rompath != "" :
		contents = os.listdir(rompath)
		for f in range(0, len(contents)) :
			if isfile(join(rompath, contents[f])) :
				listbox2.insert(END, contents[f])
	
	
	
##
#		 #
#	Main #
#		 #
##

root = Tk()
root.title('EmuMan')

frame1 = Frame(root)
frame2 = Frame(root)

listbox = Listbox(frame1, selectmode=BROWSE)
listbox2 = Listbox(frame2, selectmode=BROWSE)

frame1.pack(side="left")
frame2.pack(side="right")

text = "default"

f_reader = filereader.FileReader()
f_reader.read_config()
num_consoles = f_reader.get_num_consoles()

for x in range(0, num_consoles) :
	text = f_reader.get_console(x)
	listbox.insert(END, text)

listbox.pack()
listbox2.pack()

window = Label(root, text="Hello, world!")
window.pack()

button = Button(root, text="Start", command=run_game)
button.pack()

listbox.bind("<ButtonRelease-1>", updatelist)

root.mainloop()
