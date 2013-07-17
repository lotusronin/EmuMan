# File: filereader.py

import configparser

file_name = "/home/marcus/Programming/EmuMan/config.txt"

class FileReader:
	
	def read_config(self):
		
		try :
			self.config = configparser.ConfigParser()
			self.config.readfp(open(file_name))
			
		except IOError:
			print("Config file not found.\nMaking new file")
			f = open(file_name, 'w')
			f.write("# This is a config file for EmuMan")
			f.close()



	def ret_path(self, n) :
		section_list = self.config.sections()
		return self.config.get(section_list[n], "emupath")
	
	
	
	def ret_rom(self, n) :
		section_list = self.config.sections()
		return self.config.get(section_list[n], 'rompath')



	def get_num_consoles(self) :
		section_list = self.config.sections()
		x = 0
		for item in section_list :
			x += 1
		return x


	def get_console(self, n) :
		section_list = self.config.sections()
		return self.config.get(section_list[n], 'console')
	
