# DVR3D-python-interface
This interface is designed to be run on Linux for the DVR3D Fortran library.

* [Environment](#environment)
* [Compile](#compile)
* [Run](/DVR3Dinterface/)
* [Input Format](/DVR3Dinterface/input/)
* [Config Files](/DVR3Dinterface/configs/)


# Environment
Requires:
* Python 3.8
* "fortranformat" available from pip install

Other version of python higher than 3.2 should still work.

# Compile
While running from console, note that python does compiling and run together by 

"python script.py [some arguments]"

## Compiled binary
It is a file named "parse" in same folder as parse.py provided as a test.
It is expected to be able to run without python compiler and any python packages. But for some reason the file is larger than expected (12Mb)
Detaile use instruction can be found in [it's folder](/DVR3Dinterface/)'s README file

