from fortranformat import FortranRecordWriter as ffW
from pathlib import Path
import json
import os

# Print warning if input type and output data type is different
def formatCheck(data,formatstr,varname):
    if (formatstr[0] in ['F','D','f','d','E','e'] and type(data)!=float) \
        or (formatstr[0] in ['I','i'] and type(data)!=int)\
        or (formatstr[0] in ['L','l'] and type(data)!=bool) \
        or (formatstr[0] in ['A','a'] and type(data)!=str):
        print("Warning: Output format for {} is {}, given {}".format(varname, formatstr, type(data)))

class GeneralParser:
    config = {}

    def __init__(self,config):
        with open (Path(config)) as f:
            self.config=json.load(f)

    def __PrtToStr(self,name,bol):
        if bol:
            name += "=.true., "
        else:
            name += "=.false., "
        return name
    
    # Parse and print the NAMELIST line
    def __parPRT(self,configsub,data,filestream):
        filestream.write(" {} ".format(configsub["head"]))
        # Check if Int type keylist is present in config
        if "keylist_I" in configsub:
            # Loop and print
            for var in configsub["keylist_I"]:
                if var in data:
                    if type(data[var]) != int: raise TypeError("Type of {} must be int, got: {}".format(var, data[var]))
                    filestream.write(var.lower()+"={}, ".format(data[var]))

        # Check keylist_A, all optional
        if "keylist_A" in configsub:
            for var in configsub["keylist_A"]:
                if var in data:
                    filestream.write(var.lower()+"={}, ".format(data[var]))
        
        # Check keylist_L, all optional
        for var in configsub["keylist_L"]:
            if var in data:
                filestream.write(self.__PrtToStr(var.lower(),data[var]))
        
        # Change Line, and write the "/" at the end of first line.
        filestream.write(" / \n")

    # Parse the variable line
    # All variable should have same type
    def __parVAL(self,configsub,data,filestream):
        countval = 0
        writer = ffW(configsub["format"])
        for var in configsub["keylist"]:
            if var in data:
                # Format check
                formatCheck(data[var],configsub["format"],var)

                filestream.write(writer.write([data[var]]))
                countval+=1
            elif countval<configsub["minval"]:
                raise KeyError("Mandatory variable not provided: {}".format(var))
            else:
                break

        filestream.write("\n")

    # Print title
    def __parTITLE(self,configsub,data,filestream):
        if len(data["TITLE"]) > configsub["length"]:
            print("Warning: Title longer than config set length, will be capped")
        filestream.write(data["TITLE"][:configsub["length"]]+"\n")

    # Customised format
    def __parCUS(self,configsub,data,filestream):
        countval = 0
        for var in configsub["keylist"]:
            if var in data:
                # Format check
                formatCheck(data[var],configsub["keylist"][var],var)

                writer = ffW(configsub["keylist"][var])
                filestream.write(writer.write([data[var]]))
                countval+=1
            elif countval<configsub["minval"]:
                raise KeyError("Mandatory variable not provided: {}".format(var))
            else:
                break

        filestream.write("\n")


    def write(self,input,output):
        with open (Path(output),"w+",encoding="utf-8") as f:
            for line in self.config:
                try:
                    if self.config[line]["type"] == "PRT":
                        self.__parPRT(self.config[line],input,f)
                    elif self.config[line]["type"] == "VAL":
                        self.__parVAL(self.config[line],input,f)
                    elif self.config[line]["type"] == "TITLE":
                        self.__parTITLE(self.config[line],input,f)
                    elif self.config[line]["type"] == "CUS":
                        self.__parCUS(self.config[line],input,f)
                    else:
                        raise ValueError("Config type not found: {}".format(line))
                except Exception as e:
                    print("Error parsing {}: {}".format(line,e))
                    raise

def txtToJson(filepath):
    pathin = Path(filepath)
    pathout = Path(filepath+".json")
    with open(pathin,"r",encoding="utf-8") as fin:
        with open(pathout,"w+",encoding="utf-8",newline="") as fout:
            fout.write("{\n")
            line = fin.readline()
            firstline = True # Don't print the first comma
            while(line):
                try:   
                    if (line and not (line[0]=='!' or line == "\n") and not firstline): fout.write(",")
                    # This will allow comment line
                    if line[0]=='!' or line == "\n": 
                        line = fin.readline()
                        continue

                    firstline = False
                    lineVec = line.split(":")
                    fout.write("\"{}\":{}".format(lineVec[0],':'.join(lineVec[1:])))
                    line = fin.readline()
                    
                except Exception as e:
                    print("Failed reading input, check file format: {}".format(line))
                    raise
            fout.write("}")
    return pathout