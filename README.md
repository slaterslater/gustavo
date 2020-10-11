## Get-Url-Status (GUS) Text-As-Visual-Output (TAVO)
GUS is a command line tool that searches a file for all HTTP URLs and generates a report of their status.
### Requirements
1. Install Python 3.0 or greater. You can find the latest release at [www.python.org](https://www.python.org/downloads/)
2. Download or clone this repo
3. Open a terminal
### Usage
GUS can be used from the command line or python shell.\
The location to a source file must be supplied.
#### From the python shell
```
>>> import gus
>>> gus.tavo('FILENAME')
```
#### From the command line
```
$ python gus.py [-f FILENAME]
```
Optional command line arguments | Description
--|--
-f FILENAME, --file FILENAME | location of source file to be checked
-a, --all | output includes all results (this is default)
-g, --good | output includes only [GOOD] results
-b, --bad | output includes only [FAIL] results
-r, --rtf | output as colourized rich text file
-j, --json | output as JSON
-h, --help | show information on how to use the tool and exit
-v, --version | show program's version number and exit
### Results
GUS makes an HTTP connection for each URL in the source file.\
The header is requested and the response code determines which label will be applied:
* 2xx is [GOOD]
* 4xx is [FAIL]
* All other codes will be marked as [UNKN]

GUS can generate **output.rft** as a list of results colourized as follows:
* [GOOD] is green 
* [FAIL] is red
* [UNKN] is grey