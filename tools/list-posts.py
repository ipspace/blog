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
from datetime import date, datetime, timezone
import common

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='List posts in a directory(tree) by publish date')
  parser.add_argument('dir', action='store',help='Directory to list')
  parser.add_argument('--log', dest='logging', action='store_true',
                  help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
                  help='Enable more verbose logging')
  return parser.parse_args()

def read_file(path,dir_list):
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)
  date = frontmatter.get('date')
  if frontmatter.get('draft'):
    date = None

  dir_list.append({
    'name': os.path.basename(path),
    'date': date
    })

def scan_posts(path,dir_list):
  if LOGGING:
    print("Scanning %s" % path)

  with os.scandir(path) as dir:
    for entry in dir:
      entry_path = os.path.join(path,entry.name)
      if entry.is_dir():
        if not entry.name.startswith('.'):
          scan_posts(entry_path,archive,tags)
      elif entry.is_file():
        read_file(entry_path,dir_list)
  return dir_list

def print_dir(dir_list):
  last_day = -1
  for entry in dir_list:
    date = entry['date']
    wday = date.weekday()
    if wday < last_day:
      print("-----")
    last_day = wday
    print("%15s: %s" % (date.strftime('%a %Y-%m-%d %H:%M'),entry['name']))

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

dir_list = sorted(scan_posts(args.dir,[]),key=lambda x: x['date'])
print_dir(dir_list)

#for t in sorted(tags.keys(), key=lambda x: tags[x].weight, reverse=True):
#  print("%-20s %f %i" % (t,tags[t].weight,tags[t].count))