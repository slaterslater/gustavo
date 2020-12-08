## Get-Url-Status (GUS) Text-As-Visual-Output (TAVO)
GUS is a command line tool that searches a file for all HTTP URLs and generates a report of their status.
### Usage
```
$ python gus.py [-f FILENAME]
```
Optional command line arguments | Description
--|--
-f FILENAME, --file FILENAME | location of source file to be checked
-t, --telescope | check recent posts indexed by Telescope
-a, --all | output includes all results (this is default)
-g, --good | output includes only [GOOD] results
-b, --bad | output includes only [FAIL] results
-r, --rtf | output as colourized rich text file
-j, --json | output as JSON
-h, --help | show information on how to use the tool and exit
-v, --version | show program's version number and exit
-i FILENAME, --ignore FILENAME | location of file with list of domains to ignore
### Results
GUS makes an HTTP connection for each URL in the source file.\
The header is requested and the response code determines which label will be applied:
* [GOOD] = 2xx series
* [FAIL] = 4xx series 
* [UNKN] = all other code series

GUS can generate **output.rft** as a list of results colourized as follows:
* [GOOD] = green 
* [FAIL] = red
* [UNKN] = grey

### Setup
For information on system requirements and how to contribute, check out [CONTRIBUTING.md](CONTRIBUTING.md)