# release 0.1
import http.client
import re
import sys

# regex will match all urls starting with http or https
# matches include the leading character to check if url is nested in brackets etc
REGEX = r'.?http[s]?://[a-zA-Z0-9- _.~!*\'();:@&=+$,/?%#[\]]+.'
NESTED = {'(':')', '[':']', '>':'<', '"':'"'}

# main function
def tavo(source = ''):
  if len(source) == 0:
    get_help()                  # calls for help if no arg provided
  else:
    urls = get_list(source)     # creates list of all urls from provided source file
    checked = check_list(urls)  # checks if each urls is nested and then checks http status
    print_rtf(source, checked)  # prints results to output.rtf

# open file and return list of regex matches
def get_list(source):
  try:
    with open(source) as src:
      found = re.findall(REGEX, src.read())
    return found  
  except:
    print('error opening source file')

# checks first and last character against nested dictionary
def check_nested(char):
  url = char
  if(char[0] in NESTED and NESTED.get(char[0]) == char[-1]):
    url = char[1:-1]
  return url

# split the received string into protocol, domain, path
# make http connection, check head, return response code as string 
def check_status_code(url):
  print(f"checking {url}")
  part = re.split('((?<=//)[^/]*)',url)
  try:
    conn = http.client.HTTPSConnection(part[1], timeout=5)    # takes domain
    conn.request("HEAD", part[2])                             # takes path
    code = conn.getresponse().status  
    print(code)
    return str(code)
  except:
    print("something went wrong")
    return "???"    

# assigns colour from returned code string
def check_list(list):
  checked = []
  for url in list:
    url = check_nested(url)
    code = check_status_code(url)
    color = r'\cf2' #grey
    status = 'UNKN'
    if code[0] == '2':
      color = r'\cf4' #green
      status = 'GOOD'
    elif code[0] == '4':
      color = r'\cf3' #red
      status = 'WARN'
    checked.append(f"{color} [{code}] [{status}] {url}")
  print("Done!") 
  return checked

# creates an rtf file and writes results
def print_rtf(source, results):
  RTF = """{\\rtf1\\ansi\\ansicpg1252\\cocoartf2513\n
    \\cocoatextscaling0\\cocoaplatform0{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;}\n
    {\\colortbl;\\red255\\green255\\blue255;\\red87\\green87\\blue87;\\red252\\green41\\blue19;\\red159\\green242\\blue92;}\n
    {\\*\\expandedcolortbl;;\\cssrgb\\c41531\\c41531\\c41531;\\cssrgb\\c100000\\c25745\\c7993;\\cssrgb\\c67668\\c94348\\c43431;}\n
    \\vieww12000\\viewh15840\\viewkind0\n
    \\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\partightenfactor0\n
    \\f0\\fs24 \\cf0"""
  try:
    with open('output.rtf','w') as out:
      out.write(RTF + '***** HTTP status of ' + str(len(results)) + ' URLs from ' + source + ' *****\\\n\\\n' + '\\\n'.join(results) + '}')
    print('output.rtf is ready')  
  except:
    print('error writing list')

# print intructions on how to use tool
def get_help():
  try:
    help = open('help.txt').read()
    print(help)
  except:
    print("error printing help")

if __name__ == "__main__":
  if len(sys.argv) == 1:
    get_help()  # calls for help if no arg provided
  elif len(sys.argv) == 2 and str(sys.argv[1])[:1] != "-":
    tavo(str(sys.argv[1])) # send command line arg to main function
  else:
    if len(sys.argv) == 3 and (sys.argv[1] == "-f" or sys.argv[1] == "--file"):
      tavo(str(sys.argv[2])) # send command line arg to main function
    elif len(sys.argv) == 2 and sys.argv[1] == "-v" or sys.argv[1] == "--version":
      print('Get-Url-Status (GUS) Text-As-Visual-Output (TAVO) version 0.1') #print version info
    elif len(sys.argv) == 2 and sys.argv[1] == "-h" or sys.argv[1] == "--help":
        get_help()
    else:
      print('invalid argument error')
