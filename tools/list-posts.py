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
  parser = argparse.ArgumentParser(description='List posts in a directory(tree) by publish date')
  parser.add_argument('dir', nargs='*',action='store',help='Directory to list')
  parser.add_argument('--tags',dest='tags',action='store',help='Limit printout by tags')
  parser.add_argument('--series',dest='series',action='store',help='Limit printout by series')
  parser.add_argument('--md', dest='md', action='store_true',help='Markdown printout')
  parser.add_argument('--url', dest='url', action='store_true',help='URL printout')
  parser.add_argument('--file', dest='file', action='store_true',help='Filename printout')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  parser.add_argument('--prefix',dest='prefix',action='store',help='URL prefix',default='/')
  return parser.parse_args()

def read_file(path,dir_list,tag_list,series):
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)
  if frontmatter is None:
    return

  date = frontmatter.get('date')
  file_entry = {
    'name': os.path.basename(path),
    'path': path,
    'date': date,
    'tags': frontmatter.get('tags'),
    'title':frontmatter.get('title')
  }

  if frontmatter.get('draft'):
    file_entry['date'] = None
    file_entry['dir']  = date.strftime('%Y/%m')

  if tag_list:
    if not tag_filter.match_tags(frontmatter.get('tags'),tag_list):
      return

  if series:
    if not series in frontmatter.get('series',[]):
      return

  dir_list.append(file_entry)

def scan_posts(path,dir_list,tag_list,series):
  if LOGGING:
    print("Scanning %s" % path)

  for entry in glob.glob(path + "/*"):
    if VERBOSE:
      print("Inspecting %s " % entry)
    if os.path.isdir(entry):
      scan_posts(entry,dir_list,tag_list,series)
    elif os.path.isfile(entry):
      read_file(entry,dir_list,tag_list,series)
  return dir_list

def print_dir(dir_list):
  last_day = -1
  last_date = None
  today = datetime.now().date()
  for entry in dir_list:
    date = entry['date']
    wday = date.weekday() if date else -1
    if not date:
      if last_date:
        print("-----")
      color = "red"
    else:
      color = "green" if date.date() > today else "yellow" if date.date() == today else None
      if date.hour > 12:
        color = "magenta"
      if last_date != None and date.date() == last_date.date():
        color = "red"
      elif wday <= last_day:
        print("-----")
      elif wday > last_day + 1 and wday <= 5:
        print(".....")
    last_day = wday
    last_date = date
    line = "%20s: %s" % (date.strftime('%a %Y-%m-%d %H:%M') if date else f"{entry['dir']} DRAFT",entry['name'])
    print(colored(line,color) if color else line)

def print_url(sorted_list,prefix):
  for entry in dir_list:
    print("%s%s" % (prefix,entry['path']))

def print_html(dir_list,prefix):
  for entry in dir_list:
    print('* [%s](%s%s)' % (entry['title'],prefix,entry['path']))

def print_filename(dir_list):
  for entry in dir_list:
    print(entry['path'])

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

dir_list = []
tag_list = None
max_date = dateutil.parser.parse('2100-01-01 00:00:00+00')
if args.tags:
  tag_list = tag_filter.parse_tags(args.tags)
  if args.verbose:
    print(f'Limiting printout by tags {tag_list}')

if not args.dir:              # Iterate over all posts when nothing is specified
  args.dir = ['*']

for entry in args.dir:
  dir_list = scan_posts(entry,dir_list,tag_list,args.series)

sorted_list = sorted(dir_list,key=lambda x: x['date'] or max_date)
if args.md:
  print_html(sorted_list,args.prefix)
elif args.url:
  print_url(sorted_list,args.prefix)
elif args.file:
  print_filename(sorted_list)
else:
  print_dir(sorted_list)
