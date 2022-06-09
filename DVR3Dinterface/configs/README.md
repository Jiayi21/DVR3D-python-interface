# Config Files:
Config files are in json format, used to specify desired format of a .job file, which is used as input to Fortran code.

If the input format to Fortran code was updated, such as changing variable name or format from F20.0 to something else. The interface could be updated by updating config files, without touching python code.

Note: Some variable format was not verified or the working example is different from document. These information can be found in [Unvarified config](/DVR3Dinterface/configs/Unvarified_config.md)

# Config Format
~~~~
{
  "LINE1": {
    "type": "PRT",
    ....
  }
}
~~~~
Each config made up by lines, it has the same meaning as document. 

"LINE1" is the name of the line, it can have other name and affect nothing.

Each **line** must have a **type**. There are 4 types available for 4 differnt scheme of input: "PRT", "VAL", "TITLE" and "CUS"

## Line Type
### 1. PRT
~~~~
"LINE1": {
  "type": "PRT",
  "head": "&PRT",
  "keylist_A": ["TOLER"],
  "keylist_L": ["ZPFUN","ZTRAN","ZDCORE","ZDIAG"]
}
~~~~
PRT is used for NAMELIST in document, usually the first line.

All arguments in keylist of this type of line is optional. Parser will not print warning for missing any of them.

* **head**: The head of the line. Usually "&PRT" for the first line. In SPECTRA there is another namelist line, with head "&SPE"
* **keylist_A**: All possible arguments which are not Boolean type. To keep accuracy, these arguments will be read by parser as String and directly written into job file without parsing.
* **keylist_L**: Same as above, but value is only Boolean type.

---
### 2.VAL
~~~~
"LINE2": {
  "type": "VAL",
  "format": "I5",
  "minval": 1,
  "keylist": ["NVIB","NEVAL", "KMIN","IBASS","NEVAL2"]
}
~~~~

VAL is used for values in a line are of **same format**

* **keylist**: Name of possible arguments. The order in the list matters.
* **format**: Fortran format of values. All parameter in keylist will all print in this format.
* **minval**: Minimum number of value to present. 

Since all value must be given before the first missing optional argument, the input is checked in order of keylist. If a value is missing and minimum number of value was not reached, the parser will report error and terminate.

For example:
* Given NEVAL: Error
* Given NVIB: OK
* Given NVIB, NEVAL: OK
* Given NVIB, KMIN: OK but the KMIN will be ignored

---
### 3. TITLE
~~~~
"LINE3": {
  "type": "TITLE",
  "length": 72
}
~~~~
Just the title. Usually the type is 9A8 in document, but actually if it is 9 words does not affect code. Thus it is simplified to a length of 72.

If the title is longer than 72 chars. It will be capped to 72.

---
### 4.CUS
~~~~
"LINE4": {
  "type": "CUS",
  "minval": 1,
  "keylist": {
    "EZERO": "F13.8"
}}
~~~~
CUS is used for custimised line format. Similar to VAL, but argument in the line can have different format.

As shown in the piece of config above, it does not have "format", but adding a format after each argument name after ":". Different argument name should separated comma.
