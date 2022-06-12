This file includes the variables that input format hasn't been verified.

* Been verified: Fortran code can run for that variable have same format as the document
* Differ: Format on document didn't work (by error, wrong result, or that F20.0 looks greatly different from example), but an acceptable format was found (most likely manually counted from example)
* Unknown: Not verified, and does not in an example. Parsing of this variable was not tested.

# DVR3DJZ
## Unknown
FIXCOS: F20.0

EZERO: F20.0

## Differ
XMASS
  * Doc: 3F20.0
  * Exa: "F15.9","F14.1","F28.9"

XMASSR
  * Doc: 3F20.0
  * Exa: "F15.9","F14.1","F28.9"

EMAX1,EMAX2
* 2F20.0
* 2F14.1

RE1,DISS1,WE1
* 3F20.0
* "F12.1","F23.1","F19.4"

RE2,DISS2,WE2
* 3F20.0
* "F12.1","F23.1","F20.3"

# ROTLEV3
## Differ
EZERO
* F20.0
* F13.8

# DIPOLE3
## Unknown
EZEROUP: F20.0

TE: F20.0

## Differ
EZERO
* F20.0
* F13.8

# SPECTRA
## Unknown
not summaried

## DIffer
GE,GO
* 2D10.0: fortranformat has problem parseing "1.0" to this format
* 2F10.0: Can parse, but not tested, this line in example is F8.1

LINE 4:
* From: F10.0
* To: F7.1, D12.1, F10.1, F10.1, F7.1 F14.1