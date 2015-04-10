#! /usr/bin/python
# File: emuman.py

from gi.repository import Gtk
import filereader
import gamewidget
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
gamegrid = []

##
#						  #
#	Function Declarations #
#						  #
##

def updatelistGTK(widget, event) :
	global conf
	global flow
	global win
	global emupath
	global rompath
	
	print("UPDATING GTK LIST!!!!!")
	
	option = (combo.get_active_text()).split()
	emupath = conf.ret_path(int(option[0]))
	rompath = conf.ret_rom(int(option[0]))

	print(rompath)
	"""
	listbox2.delete(0,END)
	"""
	if rompath != "" :
		contents = os.listdir(rompath)
		for f in range(0, len(contents)) :
			if isfile(join(rompath, contents[f])) :
				"""
                h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                h.add(Gtk.Label(contents[f]))
                """

				tile = gamewidget.GameLabel(contents[f],"Game!","")
				gamegrid.append(tile)
				print(contents[f])
				#flow.add(h)
				tile.setCallback(run_game_new)
				flow.add(tile.getWidget())
	win.show_all()


def run_gameGTK(widget) :
	print("RUNNING GAME!!!!")
	global win
	global rompath
	global emupath
	global rom
	global flow
	
	widgets = flow.get_selected_children()
	rom = widgets[0].get_children()[0].get_children()[0].get_text()
	print(rom)
	
	if rom == "" or rompath == "" or emupath == "" :
		print("Error, not a valid choice")
	else :
		win.hide()
		win.queue_draw()
		while(Gtk.events_pending()) :
			Gtk.main_iteration()
		st = emupath + ' "' + rompath + rom + '"'
		#print(st)
		os.system(st)
		win.show()

def run_game_new(widget, rom_name) :
	print("RUNNING GAME!!!!")
	global win
	global rompath
	global emupath
	global rom
	global flow
	
	rom = rom_name
	print(rom)
	
	if rom == "" or rompath == "" or emupath == "" :
		print("Error, not a valid choice")
	else :
		win.hide()
		win.queue_draw()
		while(Gtk.events_pending()) :
			Gtk.main_iteration()
		st = emupath + ' "' + rompath + rom + '"'
		#print(st)
		os.system(st)
		win.show()


def delete_row(widget) :
	global glistbox2
	print("Deleting Row!!!!")
	glistbox2.remove(widget)

##
#		 #
#	Main #
#		 #
##

win = Gtk.Window()
header = Gtk.HeaderBar()
header.props.show_close_button = True
header.props.title = "Emuman"
win.set_titlebar(header)
win.connect("delete-event", Gtk.main_quit)
win.set_default_size(240,160)

grid = Gtk.Grid()
vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
vbox.pack_start(hbox, False, True, 0)
#vbox.add(grid)
win.add(vbox)

frame1 = Gtk.Frame(expand=False)
frame3 = Gtk.Frame(expand=False)

button1 = Gtk.Button("Start")

store = Gtk.ListStore(int, str)


combo = Gtk.ComboBoxText()
frame1.add(combo)
frame3.add(button1)

scrolled = Gtk.ScrolledWindow()
scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
flow = Gtk.FlowBox()
flow.set_valign(Gtk.Align.START)
flow.set_max_children_per_line(30)
scrolled.add(flow)


vbox.pack_start(scrolled, True, True, 0)
hbox.pack_end(frame1, False, True, 0)
hbox.pack_end(frame3, False, True, 0)

text = "default"

conf = filereader.FileReader()
conf.read_config()
num_consoles = conf.get_num_consoles()

for x in range(0, num_consoles) :
	text = conf.get_console(x)
	hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
	hb.add(Gtk.Label(x))
	hb.add(Gtk.Label(text))
	combo.append_text(str(x)+" "+text)

combo.connect("changed", updatelistGTK, None)
button1.connect("clicked", run_gameGTK)

win.show_all()
Gtk.main()
