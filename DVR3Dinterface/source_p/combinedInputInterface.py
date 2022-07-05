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
    """
    Main interface to process Batch data (multiple steps) using single step parsing class

    Attributes:
    -----------
        commands        [[str]]     A List of List of commands. Includes Fortran running and other commandline instructions (such as cp)
        commands_grp    [str]       Cache a group of commands before put into "commands"
        RE_PAIRs        [[Tuple]]   A list of List of Tuples of filenames to be renamed from & to
        RE_PAIRs_grp    [Tuple]     Cached group
        LK_PAIRs        [[Tuple]]   A list of List of Tuples of filenames to be Linked from & to
        LK_PAIRs_grp    [Tuple]     Cached group
        JROT,IDIA,PROJECT_NAME      Only affect renamed filename
        saveOptional    [Bool]      If optional fort.X should be renamed and saved

    Methods:
    --------
        __init__        Actually not Initializing, but do all the parsing and save all commands to be run later.
        printCommands   Print the Attribute "commands" in a better layout, usually for debug using
        run             Run the saved commands.
    """
    # Record the commandline to run
    commands = [] # A List of List of commands. This two-level structure allows execute all commands group by group
    commands_grp = [] # cache a number of blocks before been put into commands
    # renaming pairs for the output fort.X files
    RE_PAIRs = []
    RE_PAIRs_grp = []
    # link pairs
    LK_PAIRs = []
    LK_PAIRs_grp = []
    # Three parameters affecting output filename
    JROT = "x"
    IDIA = "x"
    PROJECT_NAME = "Unknown"
    # Save all optional output files or not
    saveOptional = False

    def __init__(self,inputpath,clearcmds=True,saveOptional = False):
        """
        Do all the parsing. Prepare the instructions or renaming settings to run later

        Arguments:
        ----------
            inputpath   [str]       Path to batch input file
            clearcmds   [bool]      Result of lacking "initalizing", reset the class's attributes
            saveOptional[bool]      Save optional fort.X files (rename them) or not.
        """
        self.saveOptional = saveOptional

        tempdir ="input/temp/"
        if testmode:
            tempdir = "DVR3Dinterface/tests/testtemp/"

        # While doing test, the class was inited many times, but commands are duplicated for some reason
        if clearcmds:
            self.commands=[]
            self.commands_grp = []
            self.LK_PAIRs = []
            self.LK_PAIRs_grp = []
            self.RE_PAIRs = []
            self.RE_PAIRs_grp = []

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
            elif line[:2] != "&&" and line[:1] !="!":
                print("Warning: This line does not belong to any block: \n{}".format(line))
            # Check if is a new Fortran block
            elif line[2:9]=="Fortran":
                taskcounter+=1
                sepLine = line[10:].split(" ")
                    
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
                    dvrparser.write(jsonobj, tempdir+"tempjob{}.job".format(taskcounter),noAsk=True)
                except Exception as e:
                    print("Error at writing job file of task {}".format(taskcounter))
                    raise

                # Update the default filenames
                [self.PROJECT_NAME,self.JROT,self.IDIA] = dvrparser.getFileNamePRT()

                # gather commands to rename required files, already generated in dvrparser
                self.RE_PAIRs_grp.extend(dvrparser.RE_PAIRs) 
                self.LK_PAIRs_grp.extend(dvrparser.LK_PAIRs)

                # Optional argument:
                outname = "result_{}_J{}D{}.{}".format(self.PROJECT_NAME,self.JROT,self.IDIA,sepLine[0])
                try:
                    # Check for optional argument
                    if len(sepLine)>2:
                        for argstr in sepLine[2:]:
                            [arg, val] = argstr.split("=")
                            if arg=="outname": outname = val
                except Exception as e:
                    print("Error reading block argument: {}".format(line))
                    raise

                # add a command to this object's command list
                self.commands_grp.append("{} <input/temp/tempjob{}.job> {}".format(sepLine[1],taskcounter,outname))

            elif line[2:9]=="Execute":
                # An Execute in input means execute all everything before last Execute
                # Here we put group of commands in to that "List of List", then it can be run by groups later
                self.commands.append(self.commands_grp)
                self.commands_grp = []
                self.RE_PAIRs.append(self.RE_PAIRs_grp)
                self.RE_PAIRs_grp = []
                self.LK_PAIRs.append(self.LK_PAIRs_grp)
                self.LK_PAIRs_grp = []
            # If not &&Fortran, then it is a command to directly run
            else:
                self.commands_grp.append(line[2:])
            
            # Next line
            linecounter+=1
    
    def printCommands(self):
        for cmds in self.commands:
            for cmd in cmds:
                print(cmd)
            print("=========")

    def run(self, clearTemp = True, clearAll = False):
        """
        Run the prepaired commands, or run via OS lib.

        Arguments:
        ----------
            clearTemp   [bool]  If the temp job file and txt,json segmented from the combined input file should be deleted
            clearAll    [bool]  If the rest of fort.X files should be deleted after some of them has been renamed (saved)

        Commands will be run Group by Group, each group is the jobs before each "Execute" in input file
        Running process:
            1. Link files
            2. Execute Fortran and Other (&& + any command in input) command
            3. Unlink files
            4. Renaming fort.x files
            5. Delete all fort.x files [optional]
        """

        # This is a checking step, ensure number of groups are same. If coding correct it should be.
        if len(self.RE_PAIRs) != len(self.commands):
            print("Warning: Renaming and Executing commands have different number of groups")
        if len(self.LK_PAIRs) != len(self.commands):
            print("Warning: Linking and Executing commands have different number of groups")

        # Loop groups
        for i in range(len(self.commands)):
            
            # Do LINK operation before start running this group's command
            for lkpair in self.LK_PAIRs[i]:
                try:
                    os.link(lkpair[0],lkpair[1])
                except Exception:
                    # If linking failed, should stop running because either wrong file or no file will be given to Fortran
                    print("Failed linking: {}".format(lkpair))
                    raise

            # Loop instructions in group
            for cmd in self.commands[i]:
                code = os.system(cmd)
                if code != 0:
                    raise RuntimeError("Error code {} on running: {}".format(code,cmd))

            # Unlink
            for lkpair in self.LK_PAIRs[i]:
                try:
                    os.unlink(lkpair[1])
                except Exception:
                    print("Failed Un-Linking: {}".format(lkpair))
                    raise

            # Remove duplicated renaming commands     
            self.RE_PAIRs[i] = list(set(self.RE_PAIRs[i]))
            for cmd in self.RE_PAIRs[i]:
                try:
                    os.rename(cmd[0],cmd[1])
                except Exception:
                    print("Warning: Failed renaming: {}".format(cmd))
                    pass

            # Delete all fort.X file (renamed will not be affected)
            if clearAll:
                for f in os.listdir():
                    if f[:5] == "fort.":
                        try:
                            os.remove(Path(f))
                        except Exception:
                            print("Failed to remove: {}".format(f))
                            pass

        if clearTemp:
            dir = Path("input/temp")
            for f in os.listdir(dir):
                try:
                    os.remove(dir.joinpath(f))
                except Exception:
                    print("Failed to remove: {}".format(f))
        
