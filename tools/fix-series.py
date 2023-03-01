#!/usr/bin/env python3
#

import sys
import os
import argparse
import yaml
import common
import subprocess

def parseCLI():
  parser = argparse.ArgumentParser(description='Fix netlab tagging')
  parser.add_argument('files', nargs='+',action='store',help='Files to check')
  return parser.parse_args()

def fix_netlab_file(fname):
  if not(os.path.isfile(fname)):
    raise RuntimeError('File does not exist: %s' % fname)

  (file,ext) = os.path.splitext(fname)
  if ext != ".md":
    raise RuntimeError('File is not an MD file: %s' % fname)

  (post,html) = common.read_blog_post(fname)

  if not(html):
    raise RuntimeError('Cannot get HTML text from %s' % fname)

  old_yaml = yaml.dump(post,allow_unicode=True)
  if not post.get('series',None):
    return

  if isinstance(post['series'],str):
    post['series'] = [ post['series'] ]

  post['series'] = [ x.replace('\xa0','') for x in post['series'] ]

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
  if fix_netlab_file(fname):
    print(f"... fixed {fname}")
