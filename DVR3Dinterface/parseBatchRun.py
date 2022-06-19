import argparse
import source_p.combinedInputInterface as CII

if __name__ == '__main__':
    # This parser is the commandline parser, not the DVR3D input parser
    parser = argparse.ArgumentParser(description="Parse and run a batch of steps.\n \
                                                  Note that if there are existing files in input/temp/, \n \
                                                  they will not be removed and might be overwritten")
    parser.add_argument("input",help="Path to the input file, for example: input/combined.txt")
    parser.add_argument("-t","--temp",action="store_true",help="Everything in temp will be cleared by default. If set, they will not be removed.")
    parser.add_argument("-c","--cmds",action="store_true",help="If set, print the commandline instructions for debuging purpose")

    args = parser.parse_args()

    # Functional code start here
    combinedII = CII.CombinedInputInterface(args.input)

    # Optional print instructions that will be run in commandline
    if args.cmds:
        combinedII.printCommands()
    
    # Run commandline (Fortran, cp...)
    # Optional clearing temp folder
    combinedII.run(not args.temp)

