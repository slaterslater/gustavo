## Get-Url-Status (GUS) Text-As-Visual-Output (TAVO)
GUS is a command line tool that searches a file for all HTTP urls then prints a colourized report of their status.
### Requirements
1. Install Python 3.0 or greater. You can find the latest release at [www.python.org](https://www.python.org/downloads/)
2. Download or clone this repo
3. Open a terminal
### Usage
GUS can be used from the command line or python shell.\
The location to a source file must be supplied.
#### From the command line
```
python gus.py -f example.html or python gus.py --file example.html to check a file
python gus.py -v or python gus.py --version for version info
python gus.py -h or python gus.py --help for help

```
#### From the python shell
```
>>> import gus
>>> gus.tavo('example.html')
```
### Results
GUS makes an HTTP connection for each URL in the source file.\
The header is requested and the response code determines which label will be applied:
* 2xx is [GOOD]
* 4xx is [WARN]
* All other codes will be marked as [UNKN]

GUS generates **output.rft** as a list of results colourized as follows:
* [GOOD] is green 
* [WARN] is red
* [UNKN] is grey
