#!/usr/bin/env python3
#
# Scan the blog posts and create a list of URLs used in those blog posts
#

import os
import sys
import argparse
import yaml

LOGGING=False
VERBOSE=False

def parseCLI():
  parser = argparse.ArgumentParser(description='KB article creation helper')
  parser.add_argument('action', action='store',choices=['new','first','next'],help='Desired action')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def error(t: str) -> None:
  print(t)
  sys.exit(1)

def create_doc(path: str, fm: dict, text: str) -> None:
  with open(path, 'w') as stream:
    stream.write('---\n')
    yaml.dump(fm,stream)
    stream.write('---\n')
    stream.write(text)
    stream.close()

  print(f"Created {path}")

def build_fm(fname: str) -> dict:
  fm = {}
  dir = os.getcwd()
  fm['kb_section'] = os.path.basename(dir)
  fm['minimal_sidebar'] = True
  path_chunks = dir.split('/content')
  if len(path_chunks) < 2:
    error('Cannot figure out the content URL, "content" missing in current path')
  fm['url'] = path_chunks[1] + '/' + fname
  return fm

def kb_page_settings(fm: dict) -> None:
  fm['title'] = input('Page title: ')
  if 'y' in input('Any printouts in the page? [y/n]').lower():
    fm['pre_scroll'] = True

def kb_next(args: argparse.Namespace) -> None:
  fname = input('Page name without extension: ')
  fm = build_fm(fname+'.html')
  kb_page_settings(fm)
  create_doc(fname+'.md',fm,'')

def kb_first(args: argparse.Namespace) -> None:
  fname = input('Page name without extension [00-intro]: ') or '00-intro'
  fm = build_fm('')
  kb_page_settings(fm)
  toc_title = input('TOC title (default: none): ')
  if toc_title:
    fm['toc_title'] = toc_title
  idx_title = input('Index title (displayed on top page, default: none): ')
  if idx_title:
    fm['index_title'] = idx_title
  create_doc(fname+'.md',fm,'')

def kb_new(args: argparse.Namespace) -> None:
  fname = input('Directory name: ')
  if os.path.exists(fname):
    print(f'{fname} already exists, you might want to use "kb first" within the directory. Aborting...')
    return
  
  os.makedirs(fname)
  os.chdir(fname)
  kb_first(args)

def main():
  args = parseCLI()
  LOGGING = args.logging or args.verbose
  VERBOSE = args.verbose
  if args.action == 'next':
    kb_next(args)
    return
  
  if args.action == 'new':
    kb_new(args)
    return
  
  error(f'Action {args.action} not implemented yet')

try:
  main()
except KeyboardInterrupt:
  print('\nInterrupted')
  sys.exit(130)
