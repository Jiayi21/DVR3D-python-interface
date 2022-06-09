# Input Files
Input file is a text file encoded in UTF-8. Have similar format as a JSON file, with varialbe name as key and value as value. However, typing quotation marks can be inconvenient so the quotation marks on keys (variable name) will be added by parser.

Example input file is [example_rot](example_rot.txt)

# Input Format
Each line in the file consists of \[Variable name\] : \[Value\]

":" is not allowed to appear in variable name.
## NAMELIST
Namelist here means the first line started with "&PRT" or other lines in same format.
* For Boolean type value, use "true" or "false" without quotation marks
* For other types, put value in quotation marks, parser will condsider it as string and put it into job file without parsing. 
  * It has been found using 1d-4 and 0.0001 is same for Fortran code, means the non-boolean value in namelist can have different format. Thus, to prevent parsing cause change of the value and affect result, no parsing is done to this type of value.

## Other
Value can be given in format that acceptable by json loader. Include scientific notation.

However, note that Float in python is double precision by default, and value like 1.0d-40 should be written as 1.0e-40. "d" mark cannot be used.