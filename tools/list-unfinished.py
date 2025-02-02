#!/usr/bin/env python3
#
# Scan the blog posts and create a list of URLs used in those blog posts
#

import os
import sys
import argparse
import glob
import re
from termcolor import colored
from box import Box

import common

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='List unfinished series')
  parser.add_argument('dir', nargs='*',action='store',help='Directory to process')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def read_file(path: str) -> None:
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)
  if frontmatter is None:
    return

  if 'next-in-series' not in text:
    return

  match = re.search('{{<next-in-series.*?page="(.*?)"',text)
  if match is None:
    print(f'Cannot parse {path}')
    return
  
  next = match.group(1).replace('/posts','').replace('//','/')
  n_path = f'.{next}'.replace('.html','.md')
  if not os.path.exists(n_path):
    print(f'Missing {path} => {n_path}')

def scan_posts(path) -> None:
  if LOGGING:
    print("Scanning %s" % path)

  if os.path.isfile(path):
    read_file(path)
    return

  for entry in glob.glob(path + "/*"):
    if VERBOSE:
      print("Inspecting %s " % entry)
    if os.path.isdir(entry):
      scan_posts(entry)
    elif os.path.isfile(entry):
      read_file(entry)

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

if not args.dir:              # Iterate over all posts when nothing is specified
  args.dir = ['*']

for entry in args.dir:
  scan_posts(entry)
