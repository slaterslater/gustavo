## Get-Url-Status (GUS) Text-As-Visual-Output (TAVO)
GUS is a command line tool that searches a file for all HTTP urls then prints a colourized report of their status
### Requirements
1. Your system will need to have python 3 installed. You can find the latest release at <https://www.python.org/downloads/>
2. Download or clone this repo
3. Open a terminal
### Usage
GUS can be used from the command line or python shell\
The location to a source file must be supplied
#### From the command line
```
python gus.py example.html
```
#### From the python shell
```
>>> import gus
>>> gus.tavo('example.html')
```
