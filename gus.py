import args
import const as THE
import out
import sys
import urls

class Gus():
  def __init__(self, options):
    self.source = options.source
    self.wanted = options.wanted
    self.output = options.output
    self.ignore = options.ignore
    self.urlist = []
    self.get_url_status()

  def get_url_status(self):
    self.urlist = urls.get_list(self.source, self.ignore)
    self.urlist = urls.process_list(self.urlist, self.wanted, self.output)

  def tavo(self):
    send_results = out.to_rtf if self.output  == 'rtf' else out.to_console 
    send_results(self.urlist, self.output)

  # print intructions on how to use tool
def get_help():
  try:
    help = open('help.txt').read()
    print(help)
  except:
    print("error printing help")
  finally:  
    sys.exit(1)

if __name__ == "__main__":
  a = args.get_parsed()
  if a.source == '':
    get_help()
  gus = Gus(a)
  gus.tavo()