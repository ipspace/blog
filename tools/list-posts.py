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
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='List posts in a directory(tree) by publish date')
  parser.add_argument('dir', nargs='+',action='store',help='Directory to list')
  parser.add_argument('--tags',dest='tags',action='store',help='Limit printout by tags')
  parser.add_argument('--md', dest='md', action='store_true',help='Markdown printout')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  parser.add_argument('--prefix',dest='prefix',action='store',help='URL prefix',default='/')
  return parser.parse_args()

def read_file(path,dir_list,tag_list):
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)
  if frontmatter is None:
    return

  date = frontmatter.get('date')
  if frontmatter.get('draft'):
    date = None

  if tag_list is not None:
    if not tag_filter.match_tags(frontmatter.get('tags'),tag_list):
      return

  dir_list.append({
    'name': os.path.basename(path),
    'path': path,
    'date': date,
    'tags': frontmatter.get('tags'),
    'title':frontmatter.get('title')
    })

def scan_posts(path,dir_list,tag_list):
  if LOGGING:
    print("Scanning %s" % path)

  for entry in glob.glob(path + "/*"):
    if VERBOSE:
      print("Inspecting %s " % entry)
    if os.path.isdir(entry):
      scan_posts(entry,archive,tags)
    elif os.path.isfile(entry):
      read_file(entry,dir_list,tag_list)
  return dir_list

def print_dir(dir_list):
  last_day = -1
  today = datetime.now().date()
  for entry in dir_list:
    date = entry['date']
    wday = date.weekday()
    if wday < last_day:
      print("-----")
    last_day = wday
    line = "%15s: %s" % (date.strftime('%a %Y-%m-%d %H:%M'),entry['name'])
    color = "green" if date.date() > today else "yellow" if date.date() == today else None
    print(colored(line,color) if color else line)

def print_html(dir_list,prefix):
  for entry in dir_list:
    print('* [%s](%s%s)' % (entry['title'],prefix,entry['path']))

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

dir_list = []
tag_list = None
if args.tags:
  tag_list = tag_filter.parse_tags(args.tags)

for entry in args.dir:
  dir_list = scan_posts(entry,dir_list,tag_list)

sorted_list = sorted(dir_list,key=lambda x: x['date'])
if args.md:
  print_html(sorted_list,args.prefix)
else:
  print_dir(sorted_list)
