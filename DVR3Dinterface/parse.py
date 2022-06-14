import argparse
import json
from pathlib import Path
from xmlrpc.client import Boolean
from source_p.dvr3dparser import txtToJson,GeneralParser
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate job file from input file")
    parser.add_argument("input",help="Path to the input file, for example: input/example_rot.txt")
    parser.add_argument("config",help="What config to use, input same name as the json file in configs, no need to add .json")
    parser.add_argument("-o","--output",help="Name of output file, config name + .job by default")
    parser.add_argument("-j","--json",action="store_true",help="If set, the intermediate json file will not be removed")

    args = parser.parse_args()

    jsonfile = txtToJson(args.input)
    dvrparser = GeneralParser(Path("configs/"+args.config + ".json"))

    outfilename = args.config+".job"
    if (args.output):
        outfilename = args.output
    
    with open (jsonfile) as f:
        jsonin = json.load(f)
    
    if not args.json:
        os.remove(jsonfile)
    
    dvrparser.write(jsonin,Path("output/"+outfilename))
    print("Parsing successfully executed")

