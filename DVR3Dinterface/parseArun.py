import argparse
import json
from pathlib import Path
from xmlrpc.client import Boolean
from source.dvr3dparser import txtToJson,GeneralParser
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test running Fortran from python")
    parser.add_argument("input",help="Path to the input file, for example: input/example_rot.txt")
    parser.add_argument("config",help="What config to use, input same name as the json file in configs, no need to add .json")
    parser.add_argument("Fsource",help="Fortran code to compile and run")
    parser.add_argument("-o","--output",help="Name of output file, config name + .result by default")
    parser.add_argument("-j","--job",action="store_true",help="If set, the temp.job file will not be removed")

    args = parser.parse_args()

    jsonfile = txtToJson(args.input)
    dvrparser = GeneralParser(Path("configs/"+args.config + ".json"))


    
    with open (jsonfile) as f:
        jsonin = json.load(f)
    
    os.remove(jsonfile)
    
    dvrparser.write(jsonin,Path("output/temp.job"))

    if not args.job:
        os.remove("output/temp.job")

    outfilename = args.config+".job"
    if (args.output):
        outfilename = args.output

    os.system("make "+args.Fsource)
    os.system("./{} <output/temp.job> {}".format(args.Fsource, outfilename))

    print("Successfully executed")

