from __future__ import print_function
import sys
import os
import yaml

def findRootConfig(dir='.',config='config.yaml'):
  while True:
    try:
      cfile = open(config)
    except:
      print("Cannot file config file in %s, retrying..." % os.getcwd())
      os.chdir("../")
      continue

    cdata = yaml.safe_load(cfile)
    cfile.close()
    return cdata
