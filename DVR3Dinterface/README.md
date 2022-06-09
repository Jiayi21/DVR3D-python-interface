This page introduce how to run the interface code from commandline.

Command "python script.py -h" can show help message for the script.
# parser.py
This script is a separated commandline interface for the parser submodule "dvr3dparser.py".

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

## Compiled binary
Mostly same, but replace
~~~~
python .\parse.py ....
~~~~
by:
~~~~
./parse ....
~~~~