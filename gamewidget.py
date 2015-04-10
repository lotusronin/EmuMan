#! /usr/bin/python
# File: emuman.py

from gi.repository import Gtk, Gdk, GdkPixbuf
import os

##
#						  #
#	Class/Function Declarations               #
#						  #
##
class GameLabel:
    def __init__(self, game_name, description, img):
        self.dsizex = 200
        self.dsizey = 100
       
        self.loadImg(img)
        if(img is ""):
            image = Gtk.Label("Play")
        else:
            image = Gtk.Image.new_from_pixbuf(self.texture)

        self.game = game_name
        
        #Widgets for game information
        self.label = Gtk.Label()
        self.label.set_text(game_name+"\n"+description)
        self.label.set_size_request(40,10)
        self.button = Gtk.Button()
        self.button.add(image)
        self.button.set_size_request(200,100)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.vbox.set_homogeneous(False)
        self.hbox.set_homogeneous(False)
        #self.vbox.set_size_request(100,60)
        self.hbox.set_size_request(100,20)
        #self.hbox.pack_start(label, True, True, 0)
        #self.hbox.pack_start(button, True, True, 0)
        #self.vbox.pack_start(image, True, True, 0)
        self.vbox.pack_start(self.button, True, True, 0)
        self.vbox.pack_start(self.label, True, True, 0)
        #self.vbox.pack_start(self.hbox, True, True, 0)

    def loadImg(self, img_name):
        if(img_name is ""):
            return
        self.texture = GdkPixbuf.Pixbuf.new_from_file_at_size(img_name,
                self.dsizex, self.dsizey)
        return

    def getWidget(self):
        return self.vbox

    def setCallback(self, func) :
        self.button.connect("clicked", func, self.game)
