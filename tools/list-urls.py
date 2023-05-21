#!/usr/bin/env python3
#
# Scan the blog posts and create a list of URLs used in those blog posts
#

import os
import sys
import argparse
import glob
from termcolor import colored
from box import Box
import markdown
from bs4 import BeautifulSoup
import requests

import common

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='List URLs used by blog psots in a directory(tree)')
  parser.add_argument('dir', nargs='*',action='store',help='Directory to process')
  parser.add_argument('--match', dest='match', action='store',help='Select URLs matching this string')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  parser.add_argument('--print', dest='print', action='store_true',help='Print collected URLs')
  parser.add_argument('--check', dest='check', action='store_true',help='Check collected URLs')
  parser.add_argument('--base', dest='base', action='store', default='https://blog.ipspace.net',
                      help='Base URL for links within the same web site')

  return parser.parse_args()

def read_file(path: str,url_list: Box) -> None:
  if VERBOSE:
    print("Reading file %s" % path)

  (frontmatter,text) = common.read_blog_post(path)
  if frontmatter is None:
    return

  if '.md' in path:
    text = markdown.markdown(text)

  soup = BeautifulSoup(text, features="html.parser")
  urls = [a['href'] for a in soup.findAll('a')]
  for url in urls:
    if ('#' in url):
      (url,anchor) = url.split('#')
    else:
      anchor = None

    if url not in url_list:
      url_list[url] = { 'path': [ path ], 'count': 1, 'anchors': [] }
    else:
      if not path in url_list[url].path:
        url_list[url].path.append(path)
      url_list[url].count += 1

    if anchor and not anchor in url_list[url].anchors:
      url_list[url].anchors.append(anchor)

def scan_posts(path,url_list) -> None:
  if LOGGING:
    print("Scanning %s" % path)

  if os.path.isfile(path):
    read_file(path,url_list)
    return

  for entry in glob.glob(path + "/*"):
    if VERBOSE:
      print("Inspecting %s " % entry)
    if os.path.isdir(entry):
      scan_posts(entry,url_list)
    elif os.path.isfile(entry):
      read_file(entry,url_list)

def print_urls(url_list: Box):
  for url,meta in url_list.items():
    print(f'{url}\n.. {meta}')

def check_url_reachable(url: str,anchors: list = []) -> bool:
  if LOGGING:
    print(f'Checking {url}{" a:"+str(anchors) if anchors else ""}')
  try:
    response = requests.get(url, timeout=2)
    response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    OK = True
    if anchors:
      for a in anchors:
        if not a in response.text:
          print(f'Anchor {a} not found in {url}')
          OK = False
      
    return OK

  except Exception as ex:
    print(f"Fail: {url}\n.. {ex}")
    return False

def check_urls(url_list: Box,base: str):
  for url,meta in url_list.items():
    if not '://' in url:
      url = base + url
    if not check_url_reachable(url,meta.anchors):
      if len(meta.path) > 3:
        print('.. too many pages using this URL')
      else:
        for path in meta.path:
          print(f'.. {path}')

args = parseCLI()
LOGGING = args.logging or args.verbose
VERBOSE = args.verbose

url_list = Box({},default_box=True)
if not args.dir:              # Iterate over all posts when nothing is specified
  args.dir = ['*']

for entry in args.dir:
  scan_posts(entry,url_list)

if args.match:
  for k in list(url_list.keys()):
    if not args.match in k:
      del url_list[k]

if args.print:
  print_urls(url_list)
elif args.check:
  check_urls(url_list,base=args.base)
