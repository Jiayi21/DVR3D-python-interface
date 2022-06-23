This page introduce how to run the interface code from commandline.

Command "python script.py -h" can show help message for the script.
# parse.py
This script is a separated commandline interface for the parser submodule "dvr3dparser.py".

*Work on Win and Linux, tested on python 3.8*

The parser will read variable names and values from a [input file](/DVR3Dinterface/input/) file given by user. And generate a job file by specified [config](/DVR3Dinterface/configs/).
~~~~
usage: parse.py [-h] [-o OUTPUT] [-j] input config

positional arguments:
  input                 Path to the input file, for example: input/example_rot.txt
  config                What config to use, input same name as the json file in configs, no need to add .json

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Name of output file, config name + .job by default
  -j, --json            If set, the intermediate json file will not be removed
~~~~
Example:
~~~~
python .\parse.py input/example_rot.txt example_config -o example.job
~~~~
This example code will print a warning message. This is designed to show the reaction of the code when an Integer is required but given a Float.
 * Warning: Output format for NVIB is I5, given \<class 'float'\>

In this case, code will not fail and output Float converted from Int, but the warning message will be print.

## Compiled binary
Mostly same, but replace
~~~~
python .\parse.py ....
~~~~
by:
~~~~
./parse ....
~~~~

This also applied to other compiled binary

*Note: the binary executables might not up to date*

# parseArun.py
parse-and-run

Interface for testing running Fortran (actually running linux commandline) from python script.

*Work on Linux, tested on python 3.8*

usage can be found by running with -h argument.

example:
~~~~
python parseArun.py input/hcn.dvr DVR3DJZ dvr.out
~~~~

# parseBatchRun.py
Take a file that having multiple things to run as input.

Parse the argument to Fortran job and run Fortran code.

*Work on Linux, tested on python 3.8*

*On windows, try around the source code: source_p/combinedInputInterface.py, Class CombinedInputInterface. The "run()" is only for Fortran env. Rest of code can work*

Usage can be found by running with -h argument.

example:
~~~~
python parseBatchRun.py input/combined.txt -c
~~~~
