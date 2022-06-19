This file includes the variables that input format hasn't been verified.

Argument Status:
* Been verified: Fortran code can run for that variable have same format as the document
* Differ: Format on document have some uncertain (by error, wrong result, or that F20.0 looks greatly different from example), but an acceptable format was found (most likely manually counted from example)
* Unknown: Not verified, and does not in an example. Parsing of this variable was not tested.

# DVR3DJZ
FIXCOS,EZERO,XMASS,XMASSR,EMAX1,EMAX2,RE1,RE2,DISS1,DISS2,WE1,WE2

Changed from F20.0 to F20.10

## Unknown
FIXCOS

EZERO

# ROTLEV3
EZERO F20.0 => F20.10

# DIPOLE3
EZEROUP,TE,EZERO => F20.10

## Unknown
EZEROUP: F20.0

TE: F20.0

# SPECTRA
GE,GO: F10.0 => F10.5

LINE 4: F10.0=>F10:5 having problem

There is data have more than 5 digits before dot, output will be 10 of *

Use double precision scientific type: D10.2
* ***Tested With Difference*** :Some digits in original input has been capped



## DIffer
LINE 4:
* From: F10.0
* To: F7.1, D12.1, F10.1, F10.1, F7.1 F14.1
