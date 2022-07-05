from distutils.command.config import config
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
    """
    Generate job file and extract related information from a Python dict input of data, and a JSON file specifying configs.

    Attributes:
    -----------
        config:     [dict]  The loaded json config
        RE_PAIRs:   [Tuple] Tuples of filenames, for fort.X renaming via python OS lib.
        LK_PAIRs:   [Tuple] Tuples of filenames, for NAME_JxDx to fort.X linking via python OS lib.

        JROT:       [Auto]  JROT value only for filenames
        IDIA:       [Auto]  IDIA value only for filenames
        PROJECT_NAME[Auto]  Project name, only for filenames
        saveOptional[Bool]  If optional fort.X should be renamed.
    
    Methods:
    --------
        __basicInit         Common part of different initalization
        __init__            Two types, default and init with given JROT,IDIA,PROJECT_NAME
        __PrtToStr          Helps to print Boolean type to job file in format of .True.

        write               Process the input, extract information, write to a job file.

        __searchLink        Search if any file should be linked
        __prtXXX            Different functions for different config block types
        askForFileNameCheck When called, ask user to input missing filename parts
        getFileNamePRT      Pack 3 parts of filename in a [list] and return.

    Although the commandline interface parse and parseArun use this class only
    It is not designed to be used directly, i.e. have no run() method.
    This can easily be added in the future if required, by collecting code from paseArun.
    """
    # The loaded json config file
    config = {}
    # In early stage this is the console commands of copying files named "cpCMDs"
    # Now, these are Tuples of filenames, for renaming via python OS lib.
    RE_PAIRs = []
    # Link pairs, create alternate "path" to a single file. 
    # Not commands, are Tuples to be linked by OS lib.
    LK_PAIRs = []

    # Three parameters affecting output filename
    JROT = "x"
    IDIA = "x"
    PROJECT_NAME = "Unknown"
    # Save all optional output files or not
    saveOptional = False

    # A template of basic initalizer
    def __basicInit(self,config):
        self.config = {}
        self.RE_PAIRs = []
        self.LK_PAIRs = []
        with open (Path(config)) as f:
            self.config=json.load(f)

    # Basic init
    def __init__(self,config):
        self.__basicInit(config)

    # Init and set the output copy rule
    def __init__(self,config,JROT='x',IDIA='x',NAME="Unknown",svOp=False):
        self.__basicInit(config)
        self.JROT = JROT
        self.IDIA = IDIA
        self.PROJECT_NAME = NAME
        self.saveOptional = svOp

    def __PrtToStr(self,name,bol):
        if bol:
            name += "=.true., "
        else:
            name += "=.false., "
        return name

    def write(self,input,output,noAsk = False):
        """
        Take input and config, extract required information, write Fortran's job file.

        Argument:
        ---------
            input   [dict]  Input data.
            output  [str]   Path to output(job) file
            noAsk   [Bool]  If any of 3 parts of filename is missing, ask user to input or not.
        """              
        with open (Path(output),"w+",encoding="utf-8") as f:
            for line in self.config:
                try:
                    # Depend on block type, parse the input file
                    if self.config[line]["type"] == "PRT":
                        self.__parPRT(self.config[line],input,f)
                    elif self.config[line]["type"] == "VAL":
                        self.__parVAL(self.config[line],input,f)
                    elif self.config[line]["type"] == "TITLE":
                        self.__parTITLE(self.config[line],input,f)
                    elif self.config[line]["type"] == "CUS":
                        self.__parCUS(self.config[line],input,f)
                    elif self.config[line]["type"] == "RMLARY":
                        self.__parRMLARY(self.config[line],input,f)
                    elif self.config[line]["type"] == "OUTPUT_FILES":
                        self.__parOF(self.config[line],input,noAsk)
                        self.__searchLink(self.config[line],input)
                    else:
                        raise ValueError("Config type not found: {}".format(line))
                except Exception as e:
                    print("Error parsing {}: {}".format(line,e))
                    raise

    def __searchLink(self,configOF,data):
        """
        Search the input data for the filenames that should be linked.

        Arguments:
        ----------
            configOF    [dict]  Sub part of config of Output files.
            data        [dict]  All input data
        """
        for key in data:
            if key[:3] == "LK_":
                # For example LK_KVEC: HCN_J2D1.KVEC
                # the varnameLK will be KVEC
                varnameLK = key[3:]

                if varnameLK in data: # This means user have given new fort number for this file
                    # data[key] = "HCN_J2D1.KVEC", data[varnameLK] = data["KVEC"] = some int
                    self.LK_PAIRs.append((data[key], "fort.{}".format(data[varnameLK])))

                elif varnameLK in configOF["fixed"] or varnameLK in configOF["optional"] or varnameLK in configOF["input"]:
                    # This means, user didn't given new fort.x number, use default number stored in OUTPUT_FILES of config
                    fortNum = 0
                    if varnameLK in configOF["fixed"]: fortNum = configOF["fixed"][varnameLK]
                    elif varnameLK in configOF["optional"]: fortNum = configOF["optional"][varnameLK]
                    elif varnameLK in configOF["input"]: fortNum = configOF["input"][varnameLK]

                    else: raise RuntimeError("This should not happen, check coding dvr3dparser-GeneralParser-__searchLink.")

                    self.LK_PAIRs.append((data[key],"fort.{}".format(fortNum)))

                else:
                    # If failed to find the varname in both place, raise
                    raise KeyError("{} not found while parsing {}:{}".format(varnameLK,key,data[key]))


    # Parse and print the NAMELIST line
    def __parPRT(self,configsub,data,filestream):    
        """
        Parse for config block type "PRT"
        Other __partXXX also follow this format

        Arguments:
        ----------
            configsub   [dict]  A sub part of all config. Only for the current "block"
            data        [dict]  All input data
            filestream  [obj]   Python IO stream to the output job file
        """
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

    def __parOF(self,configsub,data,noAsk = False):
        # Process filename data
        # Always replace the old name if new was given.
        if "PROJECT_NAME" in data:
            self.PROJECT_NAME = data["PROJECT_NAME"]
        if "JROT" in data:
            self.JROT = data["JROT"]
        if "IDIA" in data:
            self.IDIA = data["IDIA"]
        
        # If missing any part of file name, ask user.
        if not noAsk:
            self.askForFileNameCheck()

        # Construct filename
        opfilename = "{}_J{}D{}".format(self.PROJECT_NAME,self.JROT,self.IDIA)

        # Generate cp commands
        for var in configsub["fixed"]:
            fileNum = 0
            # If input given number for this file, use the given one.
            if var in data:
                fileNum = data[var]
            # If not, use the default value stored in OUTPUT_FILES of config JSON
            else:
                fileNum = configsub["fixed"][var]

            varname = var
            # If the variable name start with I then remove it
            if varname[0] == "I": varname = varname[1:]

            self.RE_PAIRs.append(("fort.{}".format(fileNum), "{}.{}".format(opfilename,varname)))

        # The optional part
        if self.saveOptional:
            for var in configsub["optional"]:
                fileNum = 0
                # If input given number for this file, use the given one.
                if var in data:
                    fileNum = data[var]
                # If not, use the default value stored in OUTPUT_FILES of config JSON
                else:
                    fileNum = configsub["optional"][var]

                varname = var
                # If the variable name start with I then remove it
                if varname[0] == "I": varname = varname[1:]

                self.RE_PAIRs.append(("fort.{}".format(fileNum), "{}.{}".format(opfilename,varname)))
        
    def __parRMLARY(self,configsub,data,filestream):
        # Related-Maximum-Length-Array
        # Firstly used for XPECT3, Line 4

        # Verify input
        if configsub['maxlength'] not in data:
            raise ValueError("Related-Max_Length array failed to find maximum length")
        if type(data[configsub["key"]]) != list:
            raise TypeError("Related-Max_Length must be given by list, found {}".format(type(data[configsub["key"]])))
        if len(data[configsub["key"]]) > configsub['maxlength']:
            print("Warning: Related-Maximum-Length-Array given size greater than expected: {}".format(configsub["key"]))

        # Write
        writer = ffW(configsub["format"])
        for value in data[configsub["key"]]:
            formatCheck(value,configsub["format"],configsub["key"])
            filestream.write(writer.write([value]))

    # If one of the three part of file name is missing, ask user to input one
    def askForFileNameCheck(self):
        if self.PROJECT_NAME == "Unknown":
            keyin = input("Input project name: \n")
            self.PROJECT_NAME = keyin
        if self.JROT == "x":
            verified = False
            keyin = ''
            while (not verified):
                verified = True
                keyin = input("Input JROT (For filename only): \n")
                try:
                    keyin = int(keyin)
                except Exception:
                    print("JROT must be an int")
                    verified = False
                    continue
            self.JROT = keyin

        if self.IDIA == "x":
            verified = False
            keyin = ''
            while (not verified):
                verified = True
                keyin = input("Input IDIA (For filename only): \n")
                try:
                    keyin = int(keyin)
                except Exception:
                    print("IDIA must be an int")
                    verified = False
                    continue
            self.IDIA = keyin
    
    # Get Projectname, JROT, IDIA for filenaming
    def getFileNamePRT(self):  
        return [self.PROJECT_NAME,self.JROT,self.IDIA]

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