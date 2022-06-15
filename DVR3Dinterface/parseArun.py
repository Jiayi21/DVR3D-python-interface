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

    args = parser.parse_args()

    jsonfile = txtToJson(args.input)
    dvrparser = GeneralParser(Path("configs/"+args.config + ".json"))


    # Convert input file to JSON to read
    with open (jsonfile) as f:
        jsonin = json.load(f)
    
    os.remove(jsonfile)
    
    # Parse to the job file
    dvrparser.write(jsonin,Path("output/temp.job"))

    # Decide the output filename
    outfilename = args.config+".result"
    if (args.output):
        outfilename = args.output

    # Run make xxx or not
    if (args.make):
        os.system("make "+args.Fsource)

    # Run Fortran
    os.system("./{} <output/temp.job> {}".format(args.Fsource, outfilename))

    # Remove intermediate job file or not
    if not args.job:
        os.remove("output/temp.job")

    print("Executing finished")

