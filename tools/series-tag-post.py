#!/usr/bin/env python3
#

import sys
import os
import argparse
import yaml
import common
import subprocess

def parseCLI():
  parser = argparse.ArgumentParser(description='Migrate blog posts from HTML to Markdown')
  parser.add_argument('files', nargs='+',action='store',help='Files to check')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def series_tag_file(fname):
  if not(os.path.isfile(fname)):
    raise RuntimeError('File does not exist: %s' % fname)

  (file,ext) = os.path.splitext(fname)
  if ext != ".md":
    raise RuntimeError('File is not an MD file: %s' % fname)

  (post,html) = common.read_blog_post(fname)

  if not(html):
    raise RuntimeError('Cannot get HTML text from %s' % fname)

  old_yaml = yaml.dump(post,allow_unicode=True)
  common.set_series_tag(post)
  new_yaml =  yaml.dump(post,allow_unicode=True)
  if old_yaml == new_yaml:
    return None

  with open(fname,"wt") as output:
    output.write('---\n')
    output.write(new_yaml)
    output.write('---\n')
    output.write(html)
    output.close()
    return fname

args = parseCLI()
for fname in args.files:
  if series_tag_file(fname):
    print(f"... tagged {fname}")
