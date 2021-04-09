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
import dateutil
from datetime import date, datetime, timezone
from termcolor import colored
import common
import tag_filter

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='List ideas in draft folder')
  parser.add_argument('--tags',dest='tags',action='store',help='Limit printout by tags')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('-r','--ready', dest='ready', action='store_true',help='Display only drafts with status = ready')
  parser.add_argument('-i','--intro', dest='intro', action='store_true',help='Display drafts with intros')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def display_post(path,meta):
  print("%s:" % os.path.basename(path))
  if "title" in meta:
    print(meta['title'])

  if "intro" in meta:
    print("=" * 80)
    print(meta['intro'].rstrip())

  print("")

def read_file(path,tag_list):
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)
  if frontmatter is None:
    return

#  if tag_list is not None:
#    if not tag_filter.match_tags(frontmatter.get('tags'),tag_list):
#      return

  return frontmatter

def scan_posts(path,callback,args):
  if LOGGING:
    print("Scanning %s" % path)

  for entry in glob.glob(path + "/*"):
    if VERBOSE:
      print("Inspecting %s " % entry)
    if os.path.isdir(entry):
      scan_posts(entry,callback,args)
    elif os.path.isfile(entry):
      meta = read_file(entry,args.tags)
      if meta:
        if args.ready and not (meta.get('status') == 'ready'):
          continue
        if args.intro and not ('intro' in meta):
          continue
        callback(entry,meta)

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

scan_posts(path=os.path.dirname(__file__)+"/../content/draft",callback=display_post,args=args)
