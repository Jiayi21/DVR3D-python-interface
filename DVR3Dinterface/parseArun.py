import argparse
import json
from pathlib import Path
from source_p.dvr3dparser import txtToJson,GeneralParser
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test running Fortran from python")
    parser.add_argument("input",help="Path to the input file, for example: input/example_rot.txt")
    parser.add_argument("config",help="What config to use, input same name as the json file in configs, no need to add .json")
    parser.add_argument("Fsource",help="Fortran code to run")
    parser.add_argument("-o","--output",help="Name of output file, config name + .result by default")
    parser.add_argument("-j","--job",action="store_true",help="If set, the temp.job file will not be removed")
    parser.add_argument("-m","--make",action="store_true",help="If set, run make Fsource before executing Fortran code")

    parser.add_argument("--clearAll",action="store_true",help="If set, delete all fort.x file")
    parser.add_argument("--saveStream",action="store_true",help="If set, save \"optional\" stream fort.x files")
    parser.add_argument("--noAsk",action="store_true",help="If set and any of three part of Filename is missing, don't ask and use the default")
    parser.add_argument("--pName",help="Give, or overwrite project name, only affect copied fort.x file name")
    parser.add_argument("--pJROT",help="Give, or overwrite project JROT, only affect copied fort.x file name")
    parser.add_argument("--pIDIA",help="Give, or overwrite project IDIA, only affect copied fort.x file name")

    args = parser.parse_args()

    jsonfile = txtToJson(args.input)
    dvrparser = GeneralParser(Path("configs/"+args.config + ".json"))

    # Set GeneralParser's parameter to generate the copy fort commands
    if args.pName: dvrparser.PROJECT_NAME = args.pName
    if args.pJROT: dvrparser.JROT = args.pJROT
    if args.pIDIA: dvrparser.IDIA = args.pIDIA
    if args.saveStream: dvrparser.saveOptional = args.saveStream

    # Convert input file to JSON to read
    with open (jsonfile) as f:
        jsonin = json.load(f)
    
    os.remove(jsonfile)
    
    # Parse to the job file
    dvrparser.write(jsonin,Path("output/temp.job"),noAsk=args.noAsk)

    # # Display warning if either Renaming argument is unknown
    # if dvrparser.PROJECT_NAME == "Unknown": print("Warning: Project Name not given, will use Unknown")
    # if dvrparser.JROT == "Unknown": print("Warning: Project JROT not given, will use x for renaming files")
    # if dvrparser.IDIA == "Unknown": print("Warning: Project IDIA not given, will use x for renaming files")

    # Decide the output filename
    outfilename = args.config+".result"
    if (args.output):
        outfilename = args.output

    # Run make xxx or not
    if (args.make):
        os.system("make "+args.Fsource)

    # Run Fortran
    returncode = os.system("./{} <output/temp.job> {}".format(args.Fsource, outfilename))
    if returncode !=0:
        raise RuntimeError("Failure in Fortran running, code: {}".format(returncode))

    # Remove intermediate job file or not
    if not args.job:
        os.remove("output/temp.job")

    # Copy and rename some fort files
    for cpCMD in dvrparser.cpCMDs:
        rCode = os.system(cpCMD)
        if rCode !=0:
            print("Renaming failed: {}".format(cpCMD))
    
    # Delete all fort.X file (renamed will not be affected)
    if args.clearAll:
        for f in os.listdir():
            if f[:5] == "fort.":
                try:
                    os.remove(Path(f))
                except Exception:
                    print("Failed to remove: {}".format(f))

    print("Executing finished")

