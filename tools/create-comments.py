#!/usr/bin/env python3
#
# Scan the blog posts and create metadata and template files
#
# - blog archive data files
# - tag cloud (TBD)
#

import sys
import os
import argparse
import yaml
import re
from datetime import date, datetime, timezone
import dateutil.parser
from types import SimpleNamespace
from jinja2 import Environment, FileSystemLoader, Undefined, StrictUndefined, make_logging_undefined

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='Create comment markup from YAML data')
  parser.add_argument('--dir', dest='data', action='store', default='comments/',
                  help='Comment directory')
  parser.add_argument('--template', dest='template', action='store', default='templates/',
                  help='Template directory')
  parser.add_argument('--log', dest='logging', action='store_true',
                  help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
                  help='Enable more verbose logging')
  parser.add_argument('--rebuild', dest='rebuild', action='store_true',
                  help='Rebuild all comments')
  return parser.parse_args()

def failure(s):
  print(s)
  FAILED=True

def template(j2,data,dest):
  ENV = Environment(loader=FileSystemLoader('.'),trim_blocks=True,lstrip_blocks=True)
  template = ENV.get_template(j2)

  with open(dest,'w') as output:
    output.write(template.render(**data))
    output.close()

def scanPosts(path,archive,tags):
  if LOGGING:
    print("Scanning %s" % path)

#  for dir,subdirs,files in os.walk(path):
#    for f in files:
#      scanFile(os.path.join(dir,f),archive,tags)
#    for f in subdirs:
#      scanPosts(os.path.join(dir,f),archive,tags)
  with os.scandir(path) as dir:
    for entry in dir:
      if entry.is_dir():
        if not entry.name.startswith('.'):
          scanPosts(os.path.join(path,entry.name),archive,tags)
      elif entry.is_file():
        scanFile(os.path.join(path,entry.name),archive,tags)

def buildComments(path):
  for path,folders,files in os.walk(path):
    for file in files:
      if file.find('yaml') < 0:
        continue
      fname = os.path.join(path,file)
      output = fname.replace('yaml','html')
      with open(fname,'r') as input:
        data = yaml.safe_load(input)
      template(args.template+'comments.j2',data,output)
      print("Written %s" % output)

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

buildComments(args.data)
