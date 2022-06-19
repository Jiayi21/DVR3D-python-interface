import json
from pathlib import Path
from source_p import dvr3dparser as dp
import os

class CombinedInputInterface:
    # Record the commandline to run
    commands = []

    def __init__(self,inputpath,clearcmds=True):
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
                with open (Path("input/temp/temptxt{}.txt".format(taskcounter)),"w+",encoding="utf-8") as f:
                    while (linecounter+1 < len(lines) and lines[linecounter+1][:2]!="&&"):
                        linecounter+=1
                        f.write(lines[linecounter]+"\n")

                
                # convert to json
                jsonpath = dp.txtToJson("input/temp/temptxt{}.txt".format(taskcounter))

                # convert to job
                with open (jsonpath) as f:
                    jsonobj = json.load(f)
                dvrparser = dp.GeneralParser("configs/{}.json".format(sepLine[0]))
                dvrparser.write(jsonobj, "input/temp/tempjob{}.job".format(taskcounter))

                # add a command to this object's command list
                self.commands.append("{} <input/temp/tempjob{}.job> {}".format(sepLine[1],taskcounter,outname))


            # If not &&Fortran, then it is a command to directly run
            else:
                self.commands.append(line[2:])
            
            # Next line
            linecounter+=1
    
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
    