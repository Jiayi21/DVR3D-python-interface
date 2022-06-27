from doctest import testmod
import json
from pathlib import Path
testmode = False
try:
    from source_p import dvr3dparser as dp
except:
    # For testing
    from DVR3Dinterface.source_p import dvr3dparser as dp
    testmode = True
import os

class CombinedInputInterface:
    # Record the commandline to run
    commands = []
    # copy commands for the output fort.X files
    cpCMDs = []
    # Three parameters affecting output filename
    JROT = "x"
    IDIA = "x"
    PROJECT_NAME = "Unknown"
    # Save all optional output files or not
    saveOptional = False

    def __init__(self,inputpath,clearcmds=True,saveOptional = False):
        self.saveOptional = saveOptional

        tempdir ="input/temp/"
        if testmode:
            tempdir = "DVR3Dinterface/tests/testtemp/"

        # Scan for Project name, JROT and IDIA in input
        self.specialScan(inputpath)

        # While doing test, the class was inited many times, but commands are duplicated for some reason
        if clearcmds:
            self.commands=[]

        # Open the file read every line into a vector
        lines = open(Path(inputpath)).read().splitlines()

        # Hold the task number for filenames.
        taskcounter = 0
        linecounter = 0

        while (linecounter < len(lines)):
            line = lines[linecounter]

            # Ignore empty line
            if line=='':
                pass
            elif line[:2] != "&&":
                print("Warning: This line does not belong to any block: \n{}".format(line))
            # Check if is a new Fortran block
            elif line[2:9]=="Fortran":
                taskcounter+=1
                sepLine = line[10:].split(" ")

                # Optional argument:
                outname = "output{}.result".format(taskcounter)
                try:
                    # Check for optional argument
                    if len(sepLine)>2:
                        for argstr in sepLine[2:]:
                            [arg, val] = argstr.split("=")
                            if arg=="outname": outname = val
                except Exception as e:
                    print("Error reading block argument: {}".format(line))
                    raise
                    
                # Copy every line in this block to a temp file, untile next line start with &&
                with open (Path(tempdir+"temptxt{}.txt".format(taskcounter)),"w+",encoding="utf-8") as f:
                    while (linecounter+1 < len(lines) and lines[linecounter+1][:2]!="&&"):
                        linecounter+=1
                        f.write(lines[linecounter]+"\n")

                
                # convert to json
                jsonpath = dp.txtToJson(tempdir+"temptxt{}.txt".format(taskcounter))

                # convert to job
                with open (jsonpath) as f:
                    jsonobj = json.load(f)
                
                # Problem with testing path
                try:
                    dvrparser = dp.GeneralParser("configs/{}.json".format(sepLine[0]),\
                                                self.JROT,self.IDIA,self.PROJECT_NAME,self.saveOptional)
                except Exception as e:
                    if testmod:
                        dvrparser = dp.GeneralParser("DVR3Dinterface/configs/{}.json".format(sepLine[0]),\
                                                self.JROT,self.IDIA,self.PROJECT_NAME,self.saveOptional)
                    else:
                        raise
                
                # Generate .job file
                try:
                    dvrparser.write(jsonobj, tempdir+"tempjob{}.job".format(taskcounter))
                except Exception as e:
                    print("Error at writing job file of task {}".format(taskcounter))
                    raise

                # gather commands to rename required files, already generated in dvrparser
                self.cpCMDs.extend(dvrparser.cpCMDs) 

                # add a command to this object's command list
                self.commands.append("{} <input/temp/tempjob{}.job> {}".format(sepLine[1],taskcounter,outname))


            # If not &&Fortran, then it is a command to directly run
            else:
                self.commands.append(line[2:])
            
            # Next line
            linecounter+=1

    # Scan the input file, looking for PROJECT_NAME, JROT and IDIA for configuring filenames.
    def specialScan(self,inputpath):
        with open (Path(inputpath)) as f:
            lines = f.readlines()
        for line in lines:
            # Search for Project name
            if line[:12] == "PROJECT_NAME":
                # use "-1" to remove "\n", and use replace to remove " from "HCN"
                pN = str(line[13:-1]).replace("\"","")
                if self.PROJECT_NAME != "Unknown" and self.PROJECT_NAME != pN:
                    print("Warning: Multiple Project Name found, use {}, discard {}".format(self.PROJECT_NAME,pN))
                else:
                    self.PROJECT_NAME = pN
            
            # Do same for JROT and IDIA
            if line[:4] == "JROT":
                pJ = int(line[5:-1])
                if self.JROT != "x" and self.JROT != pJ:
                    print("Warning: Multiple Project JROT found, use {}, discard {}".format(self.JROT,pJ))
                else:
                    self.JROT = pJ
            if line[:4] == "IDIA":
                pI = int(line[5:-1])
                if self.IDIA != "x" and self.IDIA != pI:
                    print("Warning: Multiple Project IDIA found, use {}, discard {}".format(self.IDIA,pI))
                else:
                    self.IDIA = pI
    
    def printCommands(self):
        for cmd in self.commands:
            print(cmd)

    def run(self, clearTemp = True):
        for cmd in self.commands:
            code = os.system(cmd)
            if code != 0:
                raise RuntimeError("Error code {} on running: {}".format(code,cmd))
        
        if clearTemp:
            dir = Path("input/temp")
            for f in os.listdir(dir):
                try:
                    os.remove(dir.joinpath(f))
                except Exception:
                    print("Failed to remove: {}".format(f))

    def runCP(self, clearAll = False):
        for cmd in self.cpCMDs:
            code = os.system(cmd)
            if code != 0:
                print("Warning: Failed renaming: {}".format(cmd))
        
        # Delete all fort.X file (renamed will not be affected)
        if clearAll:
            for f in os.listdir():
                if f[:5] == "fort.":
                    try:
                        os.remove(Path(f))
                    except Exception:
                        print("Failed to remove: {}".format(f))
    