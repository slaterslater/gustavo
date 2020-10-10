import argparse
import re
import requests
import sys

VERSION = '***** Get-Url-Status (GUS) Text-As-Visual-Output (TAVO) ***** version 0.1.3'

# regex will match all urls starting with http or https
REGEX = r'.?http[s]?://[a-zA-Z0-9- _.~!*\'();:@&=+$,/?%#[\]]+.' # includes leading char in case url is nested
NESTED = {'(':')', '[':']', '>':'<', '"':'"'} 

# main function
# gets all urls from source, checks their status, determines output format
def tavo(source = '', out = 'std'):
  if len(source) == 0:
    get_help()                  
  else:
    urls = get_list(source)     
    processed = process_list(urls, out)  
    send_output = to_rtf if out == 'rtf' else to_console 
    send_output(source, processed)

# open file and return list of regex matches
def get_list(source):
  try:
    with open(source) as src:
      found = re.findall(REGEX, src.read())
    return found  
  except:
    print(f'error opening source file {source}')
    sys.exit(1)

# checks first and last character against nested dictionary
def check_nested(char):
  url = char
  if(char[0] in NESTED and NESTED.get(char[0]) == char[-1]):
    url = char[1:-1]
  return url

# request header and return HTTP response code and description
def get_status(url):
  try:
    conn = requests.head(url, timeout=2.5)
    code = conn.status_code
    series = str(code)[0]
    desc = 'UNKN'
    if series == '2':
      desc = 'GOOD'
    elif series == '4':
      desc = 'FAIL'
    return {'code':code, 'desc':desc}
  except:       # all exceptions default to status == 400
    return {'code':400, 'desc':'FAIL'}

# checks if string is nested; gets status code and decscription; applies desired format; returns processed list 
def process_list(list, out):
  processed = []
  formatted = rtf_format if out == 'rtf' else std_format
  for string in list:
    print(f'\r Checking URL {list.index(string)} of {len(list)}', end='\r')
    url = check_nested(string)
    status = get_status(url)
    processed.append(formatted(url, status['code'], status['desc']))
  print(' ' * 50, end='\r')   # clears the console line
  return processed

def std_format(url, code, desc):
  return f'[{desc}] [{code}] {url}'

def rtf_format(url, code, desc):
  color = r'\cf2' #grey 
  status = 'UNKN'
  if desc == 'GOOD':
    color = r'\cf4' #green
  elif desc == 'FAIL':
    color = r'\cf3' #red
  return f'{color} [{code}] [{status}] {url}'

# standard output
def to_console(source, results):
  print('\n'.join(results))  

# creates an rtf file and writes results
def to_rtf(source, results):
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
    sys.exit(1)

# print intructions on how to use tool
def get_help():
  try:
    help = open('help.txt').read()
    print(help)
  except:
    print("error printing help")
    sys.exit(1)

# define all CLI args here
def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--version', action='version', version=VERSION)
  parser.add_argument('-f', '--file', action='store', dest='filename', help='location of source file', default='')
  parser.add_argument('-r', '--rtf', action='store_const', dest='output_format', const='rtf', help='output as rich text file')
  return parser.parse_args()

if __name__ == "__main__":
  if len(sys.argv) == 1:
    get_help()  # calls for help if no arg provided
  else:
    args = parse_args()
    tavo(args.filename, args.output_format)