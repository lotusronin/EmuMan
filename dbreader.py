import json


class DatabaseReader:
    
    def __init__(self, fname) :
        try:
            self.f = open(fname)
            self.json_data = json.load(self.f)
            #print(self.json_data)
            self.f.close()
        except OSError as e:
            print("Cannot open ",fname)
            print(e)
        except ValueError as e:
            print("Error, database is not a valid JSON document")
            print(e)

    def get_value(self, s) :
        try:
            return self.json_data[s]
        except KeyError:
            print("No information on ",s," in database")
            return ""
        except AttributeError:
            print("database file was not read")
            return ""
