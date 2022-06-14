from fortranformat import FortranRecordWriter as ffW
from pathlib import Path
import json
import os

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
        # Check keylist_A, all optional
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
            while(line != ""):
                try:   
                    # This will allow comment line
                    if line[0]=='!': 
                        line = fin.readline()
                        continue

                    lineVec = line.split(":")
                    fout.write("\"{}\":{}".format(lineVec[0],':'.join(lineVec[1:])))
                    line = fin.readline()
                    if (line != ""): fout.write(",")
                except Exception as e:
                    print("Failed reading input, check file format: {}".format(line))
                    raise
            fout.write("}")
    return pathout