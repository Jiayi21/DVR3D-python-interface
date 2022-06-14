This file includes the variables that input format hasn't been verified.

**\[Detailed tested\]:** Because in the early stage I mixed up some error type. Some parameters in **Differ** section might not cause Fortran error, the error could from other reason that has been solved (missing file, or error was from other argument's format). Currently I'm testing them again while tring to find some information from Fortran code (I just realized this way after last meeting). Those tested ones will be marked as detailed tested.

Argument Status:
* Been verified: Fortran code can run for that variable have same format as the document
* Differ: Format on document have some uncertain (by error, wrong result, or that F20.0 looks greatly different from example), but an acceptable format was found (most likely manually counted from example)
* Unknown: Not verified, and does not in an example. Parsing of this variable was not tested.

# DVR3DJZ
## Unknown
FIXCOS: F20.0 : **Cause Error (maybe)**
* Done two tests, one is able to run and another thrown error. Not sure which and what I did wrong, maybe will test again later

EZERO: F20.0 : **Cause Error (maybe)**

## Differ
XMASS (Detailed Tested)
  * Doc: 3F20.0
  * Exa: "F15.9","F14.1","F28.9"
  * Both work, result different

XMASSR (Detailed Tested)
  * Doc: 3F20.0
  * Exa: "F15.9","F14.1","F28.9"
  * Both work, slightly difference. The differencing part seems copying input to output
~~~~
  <      Rotational  nuclear mass in AMU:    1.000000   12.000000   14.000000
---
>      Rotational  nuclear mass in AMU:    1.007825   12.000000   14.003074
~~~~

EMAX1,EMAX2 (Detailed Tested)
* 2F20.0
* 2F14.1
* Both work, same result

RE1,DISS1,WE1 (Detailed Tested)
* 3F20.0: **Cause Error**
* "F12.1","F23.1","F19.4"

RE2,DISS2,WE2
* 3F20.0
* "F12.1","F23.1","F20.3"

# ROTLEV3
## Differ
EZERO (Detailed Tested)
* F20.0
* F13.8
* Both can run, but not sure if result same

# DIPOLE3
## Unknown
EZEROUP: F20.0

TE: F20.0

## Differ
EZERO \[Detailed Tested\]
* F20.0 in document, and in Fortran code
* F13.8 in example
* Both format can work, producing different result

# SPECTRA
## DIffer
GE,GO
* 2D10.0: fortranformat has problem parseing "1.0" to this format
  * should be 1d0? or 0.1d1? The 0.1 it will not be allowd for D10.**0**
* 2F10.0: Can parse, but not tested, this line in example is F8.1
* F8.1: 10 positon will cause error

LINE 4:
* From: F10.0
* To: F7.1, D12.1, F10.1, F10.1, F7.1 F14.1
