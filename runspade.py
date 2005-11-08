#!/usr/bin/env python

import os, signal
import sys
import time
import ConfigParser
from getopt import getopt
from spade import spade_backend
from spade import SpadeConfigParser
#import spade

VERSION = "1.9b"

def print_help():
  print
  print "Usage: %s [options]" % sys.argv[0]
  print " -h, --help         display this help text and exit"
  print " -v, --version      display the version and exit"
  print " -c, --configfile   load the configuration file (default /etc/spade/spade.ini)"
  print " -j, --jabber       load the jabber configuration file (default /etc/spade/jabber.xml)"
  raise SystemExit

def print_version():
  print "SPADE %s by Javi Palanca, Gustavo Aranda, Miguel Escriva and others" % VERSION
  print "jpalanca@dsic.upv.es - http://magentix.gti-ia.dsic.upv.es/"
  raise SystemExit

if len(sys.argv) < 2: pass 
elif sys.argv[1] in ["--help", "-h"]: print_help()
elif sys.argv[1] in ["--version", "-v"]: print_version()


# Actually start the program running.
def main():
  #print dir(spade)
  print "SPADE", VERSION, "<jpalanca@dsic.upv.es> - http://magentix.gti-ia.dsic.upv.es/"
  """
  if mainconfig["usepsyco"]:
    try:
      import psyco
      print "Psyco optimizing compiler found. Using psyco.full()."
      psyco.full()
    except ImportError: print "W: Psyco optimizing compiler not found."
  """
  # default settings for play_and_quit.
  configfilename = "/etc/spade/spade.xml"
  jabberxml = "/etc/spade/jabber.xml"
  if os.name != "posix" or not os.path.exists(jabberxml) or not os.path.exists(configfilename):
	 configfilename = "etc" + os.sep + "spade.xml"
	 jabberxml = "etc" + os.sep + "jabber.xml"
	

  for opt, arg in getopt(sys.argv[1:],
                         "hv:c:j:", ["help", "version", "configfile=",
                                      "jabber="])[0]:
    if opt in ["-h", "--help"]: print_help()
    elif opt in ["-v", "--version"]: print_version()
    elif opt in ["-c", "--configfile"]: configfilename = arg
    elif opt in ["-j", "--jabber"]: jabberxml = arg


  configfile = SpadeConfigParser.ConfigParser(configfilename)

  workpath = configfile.get("jabber","workpath")
  if os.name == "posix":
	  jabberpath = workpath + "jabberd"
  else:
	  jabberpath = workpath + "jabberd.exe"

  if os.path.exists(jabberpath) and os.path.exists(jabberxml):
	jabberpid = os.spawnl(os.P_NOWAIT, jabberpath, jabberpath, '-c', str(jabberxml), '-H', str(workpath))
	#print "PID: " + str(jabberpid)

  try:
  	time.sleep(2)

  	platform = spade_backend.SpadeBackend(configfilename)
	platform.start()

	while True:
		time.sleep(1)
  except KeyboardInterrupt:
    pass
 
  del platform

  if os.name == "posix":
  	os.kill(jabberpid, signal.SIGTERM)
  	time.sleep(2)

  print "Jabber server terminated..."

if __name__ == '__main__': main()
