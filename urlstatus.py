# release 0.1
import http.client
import re
import sys

# regex will match all urls starting with http or https
# matches include the leading character to check if url is nested in brackets etc
regex = r'.?http[s]?://[a-zA-Z0-9- _.~!*\'();:@&=+$,/?%#[\]]+.'
nested = {'(':')', '[':']', '>':'<', '"':'"'}

def main():
  if (len(sys.argv)==1):
    getHelp()
  else:
    source = sys.argv[1]
    urls = getList(source)
    checked = checkList(urls)
    printRtf(source, checked)

def getList(source):
  try:
    with open(source) as src:
      found = re.findall(regex, src.read())
    return found  
  except:
    print('error getting list')

# checks first and last character against nested dictionary
def checkNested(char):
  url = char
  if(char[0] in nested and nested.get(char[0]) == char[-1]):
    url = char[1:-1]
  return url

# split the received string into protocol, domain, path
# HTTPSConnection object takes the domain string 
# return status code as a string
def checkStatusCode(url):
  print(f"checking {url}")
  part = re.split('((?<=//)[^/]*)',url)
  try:
    conn = http.client.HTTPSConnection(part[1], timeout=5)
    conn.request("HEAD", part[2])
    code = conn.getresponse().status  
    print(code)
    return str(code)
  except:
    print("something went wrong")
    return "???"    

# assigns colour from returned code string
def checkList(list):
  checked = []
  for url in list:
    url = checkNested(url)
    code = checkStatusCode(url)
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
def printRtf(source, results):
  rtf = """{\\rtf1\\ansi\\ansicpg1252\\cocoartf2513\n
    \\cocoatextscaling0\\cocoaplatform0{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;}\n
    {\\colortbl;\\red255\\green255\\blue255;\\red87\\green87\\blue87;\\red252\\green41\\blue19;\\red159\\green242\\blue92;}\n
    {\\*\\expandedcolortbl;;\\cssrgb\\c41531\\c41531\\c41531;\\cssrgb\\c100000\\c25745\\c7993;\\cssrgb\\c67668\\c94348\\c43431;}\n
    \\vieww12000\\viewh15840\\viewkind0\n
    \\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\partightenfactor0\n
    \\f0\\fs24 \\cf0"""
  try:
    with open('output.rtf','w') as out:
      out.write(rtf + '***** HTTP status of ' + str(len(results)) + ' URLs from ' + source + ' *****\\\n\\\n' + '\\\n'.join(results) + '}')
    print('output.rtf is ready')  
  except:
    print('error writing list')

def getHelp():
  try:
    help = open('README.md').read()
    print(help)
  except:
    print("error printing help")  

main()