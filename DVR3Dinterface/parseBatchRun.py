import argparse
import source_p.combinedInputInterface as CII
import os

if __name__ == '__main__':
    # This parser is the commandline parser, not the DVR3D input parser
    parser = argparse.ArgumentParser(description="Parse and run a batch of steps.\n \
                                                  Note that if there are existing files in input/temp/, \n \
                                                  they will not be removed and might be overwritten")
    parser.add_argument("input",help="Path to the input file, for example: input/combined.txt")
    parser.add_argument("-t","--temp",action="store_true",help="Everything in temp will be cleared by default. If set, they will not be removed.")
    parser.add_argument("-c","--cmds",action="store_true",help="If set, print the commandline instructions for debuging purpose")

    parser.add_argument("--clearAll",action="store_true",help="If set, delete all fort.x file")
    parser.add_argument("--saveStream",action="store_true",help="If set, save \"optional\" stream fort.x files")
    parser.add_argument("--pName",help="Give, or overwrite project name, only affect copied fort.x file name")
    parser.add_argument("--pJROT",help="Give, or overwrite project JROT, only affect copied fort.x file name")
    parser.add_argument("--pIDIA",help="Give, or overwrite project IDIA, only affect copied fort.x file name")

    args = parser.parse_args()

    # Functional code start here
    combinedII = CII.CombinedInputInterface(args.input)
    if args.pName: combinedII.PROJECT_NAME = args.pName
    if args.pJROT: combinedII.JROT = args.pJROT
    if args.pIDIA: combinedII.IDIA = args.pIDIA
    if args.saveStream: combinedII.saveOptional = args.saveStream

    # Optional print instructions that will be run in commandline
    if args.cmds:
        print("========Instructions to run==========")
        combinedII.printCommands()
        print("=====================================")
    
    # Run commandline (Fortran, cp...)
    # Optional clearing temp folder
    combinedII.run(not args.temp)


    # Delete all fort.X file (renamed will not be affected)
    if args.clearAll:
        for f in os.listdir():
            if f[:5] == "fort.":
                try:
                    os.remove(Path(f))
                except Exception:
                    print("Failed to remove: {}".format(f))

