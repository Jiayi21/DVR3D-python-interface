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
EZEROUP

TE

# SPECTRA
GE,GO: F10.0 => F10.5 : Tested, result same


LINE 4: F10.0=>F10:5 having problem

There is data have more than 5 digits before dot, output will be 10 of *

Use double precision scientific type: D10.2
* *Tested With Difference* :Some digits in original input has been capped

Use Custom Format: D10.2 for second argument, F10.3 for others
* ***Tested with Unknown Difference***: There is some difference from the original output, but can't tell if it's wrong.
~~~~
+ +--  8 lines: Program SPECTRA (version of Feb 2004)---------------|+ +--  8 lines: Program SPECTRA (version of Feb 2004)--------------
       Maximum frequency,   WSMAX = 0.90000D+04 cm-1                |       Maximum frequency,   WSMAX = 0.90000D+04 cm-1
       Minimum energy,       EMIN = 0.00000D+00 cm-1                |       Minimum energy,       EMIN = 0.00000D+00 cm-1
       Maximum energy,       EMAX = 0.18000D+05 cm-1                |       Maximum energy,       EMAX = 0.18000D+05 cm-1
       Minimum linestrength, SMIN = 0.10000D-39 D**2                |       Minimum linestrength, SMIN = 0.10000D-39 D**2
       Maximum rotations     JMAX =  500                            |       Maximum rotations     JMAX =  500
                                                                    |
        3000 transition records read from unit ITRA = 13            |         600 transition records read from unit ITRA = 13
        3000 selected and      written to unit ITEM = 16            |         600 selected and      written to unit ITEM = 16
                                                                    |
       Memory required to sort transitions     0.183 MB             |       Memory required to sort transitions     0.037 MB
                                                                    |
                                                                    |
            Sort completed successfully                             |            Sort completed successfully
                                                                    |
                                                                    |
                                                                    |
+ +--  9 lines: 0 secs CPU time used--------------------------------|+ +--  9 lines: 0 secs CPU time used-------------------------------
       Frequency range from      0.000 cm-1 to  18000.000 cm-1      |       Frequency range from      0.000 cm-1 to  18000.000 cm-1
       profile half width     1.000                                 |       profile half width     1.000
                                                                    |
                                                                    |
~~~~



## DIffer
LINE 4:
* From: F10.0
* To: F7.1, D12.1, F10.1, F10.1, F7.1 F14.1
