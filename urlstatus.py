# release 0.1
import http.client
import re
import sys

def main():
  if (len(sys.argv)==1):
    getHelp()
  else:
    urls = getList(sys.argv[1])
    processed = checkList(urls)
    writeList(processed)

# regex will match all urls starting with http or https
# match includes the leading character to check if url is nested in brackets etc
regex = r'.?http[s]?://[a-zA-Z0-9- _.~!*\'();:@&=+$,/?%#[\]]+.'
nested = {
  '(':')',
  '[':']',
  '>':'<',
  '"':'"'
}

def getList(file):
  try:
    with open(file) as src:
      found = re.findall(regex, src.read())
    return found  
  except:
    print('error getting list')

def checkNested(url):
  if(url[0] in nested and nested.get(url[0]) == url[-1]):
    return url[1:-1]
  else:
    return url

def checkStatus(url):
  print(f"checking {url}")
  part = re.split('((?<=//)[^/]*)',url)
  try:
    conn = http.client.HTTPSConnection(part[1], timeout=5)
    conn.request("HEAD", part[2])
    status = conn.getresponse().status  
    print(status)
    return str(status)
  except:
    print("something went wrong")
    return "hmm"    

def checkList(list):
  checked = []
  for url in list:
    url = checkNested(url)
    status = checkStatus(url)
    color = r'\cf2' #grey
    if status[0] == '2':
      color = r'\cf4' #green
    elif status[0] == '4':
      color = r'\cf3' #red
    checked.append(f"{color} {url}")
  print("Done!") 
  return checked

def writeList(urls):
  format = """{\\rtf1\\ansi\\ansicpg1252\\cocoartf2513\n
  \\cocoatextscaling0\\cocoaplatform0{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;}\n
  {\\colortbl;\\red255\\green255\\blue255;\\red112\\green112\\blue112;\\red251\\green0\\blue7;\\red35\\green255\\blue6;}\n
  {\\*\\expandedcolortbl;;\\cssrgb\\c51471\\c51471\\c51471;\\cssrgb\\c100000\\c0\\c0;\\cssrgb\\c0\\c100000\\c0;}\n
  \\margl1440\\margr1440\\vieww10800\\viewh8400\\viewkind0\n
  \\pard\\tx566\\tx1133\\tx1700\\tx2267\\tx2834\\tx3401\\tx3968\\tx4535\\tx5102\\tx5669\\tx6236\\tx6803\\pardirnatural\\partightenfactor0\n
  \\f0\\fs24 """
  try:
    with open('output.rtf','w') as out:
      out.write(format + '\\\n'.join(processed) + "}")
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