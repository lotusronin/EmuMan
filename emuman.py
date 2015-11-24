#! /usr/bin/python
# File: emuman.py

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import filereader
import gamewidget
import dbreader
import os
from os.path import isfile, join
import subprocess

##
#			  #
#	Variables #
#			  #
##

rompath = ""
emupath = ""
rom = ""
gamegrid = []
searchterm = ""

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
	dbfile = conf.get_db(int(option[0]))
	db = dbreader.DatabaseReader(dbfile)
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

				tile = gamewidget.GameLabel(contents[f],"Game!",db.get_value(contents[f]))
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
		while(Gtk.events_pending()) :
			Gtk.main_iteration()


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
		#subprocess.call([emupath,rompath+rom])
		subprocess.Popen([emupath,rompath+rom])
		win.show()

def search_callback(widget, flow) :
    #print(widget.get_text())
    global searchterm
    searchterm = widget.get_text()
    flow.invalidate_filter()


def game_filter(child,userdata) :
    s = child.get_children()[0].get_children()[1].get_text()
    if(searchterm is "") :
        return True
    if(searchterm.lower() in s.lower() or s.lower() in searchterm.lower()) :
        return True
    return False


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
win.set_size_request(240,160) #set minimum size

grid = Gtk.Grid()
vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
vbox.pack_start(hbox, False, True, 0)
#vbox.add(grid)
win.add(vbox)

frame1 = Gtk.Frame(expand=False)


store = Gtk.ListStore(int, str)


combo = Gtk.ComboBoxText()
frame1.add(combo)

scrolled = Gtk.ScrolledWindow()
scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
flow = Gtk.FlowBox()
flow.set_valign(Gtk.Align.START)
flow.set_max_children_per_line(30)
flow.set_filter_func(game_filter, None)
flow.set_homogeneous(True)
scrolled.add(flow)


vbox.pack_start(scrolled, True, True, 0)
hbox.pack_end(frame1, False, True, 0)
search = Gtk.Entry()
search.set_placeholder_text("Search")
hbox.pack_end(search, True, True, 0)

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
search.connect("changed", search_callback, flow)

#Grab focus from search entry
scrolled.grab_focus()

win.show_all()
Gtk.main()
