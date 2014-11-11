#! /usr/bin/python
# File: emuman.py

from gi.repository import Gtk
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
	#print(rom)
	
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
	#print(index[0])
	emupath = f_reader.ret_path(int(index[0]))
	rompath = f_reader.ret_rom(int(index[0]))
	#print(rompath)

	print(index[0])
	emupath = f_reader.ret_path(int(index[0]))
	rompath = f_reader.ret_rom(int(index[0]))
	print(rompath)
	listbox2.delete(0,END)
	
	if rompath != "" :
		contents = os.listdir(rompath)
		for f in range(0, len(contents)) :
			if isfile(join(rompath, contents[f])) :
				listbox2.insert(END, contents[f])


def updatelistGTK(widget, event) :
	global conf
	global glistbox1
	global glistbox2
	global emupath
	global rompath
	
	row = glistbox1.get_selected_row()
	print("UPDATING GTK LIST!!!!!")
	widgets = row.get_children()[0].get_children()


	emupath = conf.ret_path(int(widgets[0].get_text()))
	rompath = conf.ret_rom(int(widgets[0].get_text()))

	print(rompath)
	#glistbox2.clear()
	"""
	listbox2.delete(0,END)
	"""
	if rompath != "" :
		contents = os.listdir(rompath)
		for f in range(0, len(contents)) :
			if isfile(join(rompath, contents[f])) :
				h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
				#h.add(Gtk.Label(f))
				h.add(Gtk.Label(contents[f]))
				print(contents[f])
				glistbox2.insert(h,-1)


def run_gameGTK(widget) :
	#s
	print("RUNNING GAME!!!!")
	global glistbox2
	global win
	global rompath
	global emupath
	global rom
	

	
	row = glistbox2.get_selected_row()
	widgets = row.get_children()[0].get_children()
	rom = widgets[0].get_text()
	print(rom)
	
	if rom == "" or rompath == "" or emupath == "" :
		print("Error, not a valid choice")
	else :
		win.hide()
		win.queue_draw()
		st = emupath + ' "' + rompath + rom + '"'
		#print(st)
		os.system(st)
		win.show()


##
#		 #
#	Main #
#		 #
##

root = Tk()
root.title('EmuMan')

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)

listbox = Listbox(frame1, selectmode=BROWSE)
listbox2 = Listbox(frame2, selectmode=BROWSE)

frame1.pack(side="left", fill="both", expand=True)
frame3.pack(side="right")
frame2.pack(side="right", fill="both", expand=True)

text = "default"

f_reader = filereader.FileReader()
f_reader.read_config()
num_consoles = f_reader.get_num_consoles()

for x in range(0, num_consoles) :
	text = f_reader.get_console(x)
	listbox.insert(END, text)

listbox.pack(expand=True, fill="both")
listbox2.pack(expand=True, fill="both")

#window = Label(root, text="Hello, world!")
#window.pack()

button = Button(frame3, text="Start", command=run_game)
button.pack()

listbox.bind("<ButtonRelease-1>", updatelist)

root.mainloop()

##
#
#	GTK3 port
#
##

win = Gtk.Window()
header = Gtk.HeaderBar()
header.props.show_close_button = True
header.props.title = "Emuman"
win.set_titlebar(header)
win.connect("delete-event", Gtk.main_quit)

grid = Gtk.Grid()
win.add(grid)

frame1 = Gtk.Frame(expand=True)
frame2 = Gtk.Frame(expand=True)
frame3 = Gtk.Frame(expand=True)

glistbox1 = Gtk.ListBox()
glistbox2 = Gtk.ListBox()
button1 = Gtk.Button("Start")
button2 = Gtk.Button("Roms")
#button3 = Gtk.Button("Emulators")

#row = Gtk.ListBoxRow()
row2 = Gtk.ListBoxRow()

#row.add(button3)
row2.add(button2)

#listbox1.add(row)
glistbox2.add(row2)

frame1.add(glistbox1)
frame2.add(glistbox2)
frame3.add(button1)

grid.add(frame1)
grid.add(frame2)
grid.add(frame3)


text = "default"

conf = filereader.FileReader()
conf.read_config()
num_consoles = conf.get_num_consoles()

for x in range(0, num_consoles) :
	text = conf.get_console(x)
	hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
	hb.add(Gtk.Label(x))
	hb.add(Gtk.Label(text))
	glistbox1.insert(hb,-1)

glistbox1.connect("row_activated", updatelistGTK)
button1.connect("clicked", run_gameGTK)

win.show_all()
Gtk.main()