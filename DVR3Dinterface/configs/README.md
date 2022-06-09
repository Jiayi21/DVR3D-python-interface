# Config Files:
Config files are in json format, used to specify desired format of a .job file, which is used as input to Fortran code.

If the input format to Fortran code was updated, such as changing variable name or format from F20.0 to something else. The interface could be updated by updating config files, without touching python code.

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
