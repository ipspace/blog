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
import json
import glob
from datetime import date, datetime, timezone
from termcolor import colored
import common
import tag_filter

LOGGING=False
VERBOSE=True
ERRORS=False

def parseCLI():
  parser = argparse.ArgumentParser(description='Check Markdown files (blog posts)')
  parser.add_argument('files', nargs='+',action='store',help='Files to check')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def reportError(err,path):
  global ERRORS
  print("%s in %s" % (err,path))
  ERRORS=True

def check_duplicate_date(path,date):
  prefix = os.path.dirname(path)
#  if VERBOSE:
#    print("Checking duplicate date for %s in %s" % (path,prefix))

  for entry in glob.glob(prefix + "/*"):
    if entry != path:
#      if VERBOSE:
#        print("Inspecting %s " % entry)
      if os.path.isfile(entry):
        (pfront,ptext) = common.read_blog_post(entry)
      pdate = pfront.get("date")
      if pdate and pdate.date() == date.date():
        reportError("Publication date %s overlaps with %s" % (date.date(),entry),path)

def check_file(path):
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)

  if text is None:
    reportError("Markdown file is probably missing frontmatter",path)
    return

  if "localhost:1313" in text.lower():
    reportError("Localhost link",path)

  if "wwwint.ipspace.net" in text.lower():
    reportError("Link to internal web site",path)

  if frontmatter is None:
    reportError("Cannot find usable frontmatter",path)
    return

  draft = frontmatter.get('draft')

  if not(draft):
    date = frontmatter.get('date')
    if not(date):
      reportError("Date or Draft field missing",path)
    else:
      if date.hour > 10:
        print("Warning: %s scheduled for afternoon publication on %s" % (path,date.strftime("%c")))
      pathprefix = "%02i/%02i/" % (date.year,date.month)
      if path.find(pathprefix) == 0 or path.find("/"+pathprefix) >= 0:
        check_duplicate_date(path,date)
      else:
        reportError("Expected path prefix %s" % pathprefix,path)

    tags = frontmatter.get('tags')
    if type(tags) is not list:
      reportError("Tags are missing or not a list",path)

    if not(frontmatter.get('title')):
      print("Title is missing",path)

args = parseCLI()
#LOGGING = args.logging or args.verbose
#VERBOSE = args.verbose

for entry in args.files:
  if not 'series' in entry:
    check_file(entry)

if ERRORS:
  sys.exit(1)
