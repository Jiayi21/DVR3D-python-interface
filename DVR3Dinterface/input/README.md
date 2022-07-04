# Input Files
## Single File
Input file is a text file encoded in UTF-8. Have similar format as a JSON file, with varialbe name as key and value as value. However, typing quotation marks can be inconvenient so the quotation marks on keys (variable name) will be added by parser.

Example input file is [example_rot](example_rot.txt) and detailed format can be found in this page below.

## Batch (combined) input
While running multiple steps in one file, use the batch input format.

In this type of input files, for [example](combined.txt), the file is devided in to multiple **Sections**, each secion start with "&&"

### 1. Fortan DVR3D section:
~~~~
&&Fortran DVR3DJZ ./dvr.out outname=output1_manual.result
....
(Variables and values, same as single file contents)
~~~~

&& must followed by "Fortran" without spaces. It can take several arguments:
 * Config: (DVR3DJZ) config of .job file, use json filenames from configs folder without ".json"
 * Fortran Executable: (./dvr.out) Path to fortran code to run
 * \[Optional\]: Output filename, followed by "outputname=" If not given, it will be result_\<PROJECT_NAME\>J<>D<>_\<config_name\>, such as *result_HCN_J2D1.DVR3D*

### 2. Commandline Instruction Section
If there is no "Fortran" after "&&", it is a command section.

Things after "&&" of that line will be considered as a command to run 

~~~~
&&cp fort.8 fort.11
&&cp fort.9 fort.12
~~~~

### 3. "&&Execute"
As mentioned before, each instruction start with "&&" is a **Section**

All Sections above an &&Execute is a **Block**

The interface will run instructions and working steps block by block, following these steps of each block:
  1. Link files to fort.x
  2. Execute Fortran and Other (&& + any command in input) command
  3. Unlink files
  4. Renaming fort.x files
  5. Delete all fort.x files \[optional\]

If there is only one block in the combined input file, it should still have an &&Execute at the end of it.

## Extra: File Renaming
Interface will find, overwrite and cache "PROJECT_NAME", "JROT" and "IDIA" to form the renaming steps. 
* In single file situation, piority of command line given is higher than file.
* In Batch situation, please ensure the first Fortran **Section** in each **Block** provide, or update these information even if the fortran code doesn't need them.

# Input Format
Each line in the file consists of \[Variable name\] : \[Value\]

":" is not allowed to appear in variable name.
## NAMELIST
Namelist here means the first line started with "&PRT" or other lines in same format.
* For Boolean type value, use "true" or "false" without quotation marks
* For other types, put value in quotation marks, parser will condsider it as string and put it into job file without parsing. 
  * It has been found using 1d-4 and 0.0001 is same for Fortran code, means the non-boolean value in namelist can have different format. Thus, to prevent parsing cause change of the value and affect result, no parsing is done to this type of value.

## Linking files
For both batch and single file, user can Link an exist file to fort.X before executing and it will be un-linked after executing.

The way to specifying linking is:\
LK_VARNAME: "LinkFrom"

For example, the linking test file for HCN [combined_LinkTest.txt](combined_LinkTest.txt) wrote:
~~~~
LK_IKET:"HCN_J2D1.KVEC"
LK_IBRA:"HCN_J2D1.KVEC2"
IKET:8
IBRA:9
~~~~

Two linking lines are added for test and IKET,IBRA value was originally given \
(If not given, default will be used.)\
The interface will link file "HCN_J2D1.KVEC" to "fort.8"\
and "HCN_J2D1.KVEC2" to fort.9

## Other
Value can be given in format that acceptable by json loader. Include scientific notation.

However, note that Float in python is double precision by default, and value like 1.0d-40 should be written as 1.0e-40. "d" mark cannot be used.

## Comment
Comment can be used within input files, a line started by "!" will be comment and will not be read as data.

It will be useful to add some comment as separat lines in files to mark which "line" it is, or it will be hard to find variables.