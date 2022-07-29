# DVR3D-python-interface
This interface is designed to be run on Linux for the DVR3D Fortran library.

Usage:\
Except running auto-test, scripts should be run in "DVR3Dinterface" folder and so does the built Fortran executables. Source code of this python interface are in "source_p" folder, which means "source" folder can be used to store Fortran source code separatly.

* [Environment](#environment)
* [Compile](#compile)
* [Tutorial / Working Example](#tutorial--working-example)
* Detailed Documentation
  * [Run](/DVR3Dinterface/)
  * [Input Format](/DVR3Dinterface/input/)
  * [Config Files](/DVR3Dinterface/configs/) (In case the input variable to Fortran code has changed)


# Environment
Requires:
* Python 3.8 (Other version higher than 3.2 should still work.)
* "fortranformat" available from pip install

# Compile
Python is a script language, there is no compile steps and the program can be executed by:

"python script.py [some arguments]"

## Compiled binary
For example, a file named "parse" in same folder as parse.py provided as a test.

It is expected to be able to run without python compiler and any python packages. But for some reason the file is larger than expected (12Mb)
Detaile use instruction can be found in [it's folder](/DVR3Dinterface/)'s README file

*These files are not always up to date*

---
# Tutorial / Working Example
## 1. Setting up
Assuming the envrionment setting has done, this repo and the ExoMol dvr3d repo has been prepared. This example will run first 3 steps of HCN in dvr3d repo.

To setup, copy everything in DVR3Dinterface folder of this repo into the working location, that is under the HCN folder. The directory should be like:
~~~~
dvr3d/
    HCN/
        configs
        input
        .
        .
        .
        source
        source_p
        jobs
        Makefile
        parse.py
        parseArun.py
        parseBatchRun.py
~~~~

## 2. Run python script (batch)
This steps provides an idea how the scripts should be run, and a brief intro to how the interface works.

The "tasks" of running three steps (dvr, rot, dip) of HCN, with the parameters it needs has been combined into one single file: [input/HCN_ex_make.txt](DVR3Dinterface\input\HCN_ex_make.txt). Feeding this file to the "parseBatchRun.py" and the interface will generate job files as Fortran code's input and run the code.

First of all, make sure you are in working folder dvr3d/HCN, try:
~~~~
python parseBatchRun.py -h
~~~~
It shows the help message of this script. It also work on parseArun. It is a fine reminder when you foget how to run the interface.

Then:
~~~~
python parseBatchRun.py input/HCN_ex_make.txt --temp --clearAll
~~~~
Some make information will be printed. Wait to a maximum 40 secs, running should be finished. Then you can see the result_HCN_something as the result and HCN_J2D1.something as the intermediate output shown up.

## 3. Understanding the input
Have a look at the combined input if you wish: [input/HCN_ex_make.txt](DVR3Dinterface\input\HCN_ex_make.txt)

There are 4 notable points for using the interface:
### 3.1 Make and other instruction
~~~~
&&make ./dvr.out
~~~~
The first 3 lines of the input are make commands.

**Everything that not &&Fortran... or &&Execute are console instructions**

Which means: the "make ./dvr.out" is directly put into the console while the interface executing those commands. Other instructions like "cp" can also be used in this way.

### 3.2 Fortran Block
~~~~
&&Fortran DVR3DJZ ./dvr.out outname=result_HCN_J2D1.DVR3DJZ
ZROT:true
ZTRAN:true
ZLIN:true
ZTHETA:false
ZR2R1:false
...
~~~~
Each Fortran block start with &&Fortran and valid until next "&&" mark.
 * DVR3DJZ: the config name, config specify the input format of Fortran code.
 * ./dvr.out: Executable name, the compiled Fortran by the make above
 * outname: optional, specify the output's filename.

The rest of it are parameters for running.