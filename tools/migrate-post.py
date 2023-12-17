#!/usr/bin/env python3
#

import sys
import os
import argparse
import yaml
import common
import subprocess
import titlecase

def parseCLI():
  parser = argparse.ArgumentParser(description='Migrate blog posts from HTML to Markdown')
  parser.add_argument('files', nargs='+',action='store',help='Files to check')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def htmlToMarkdown(html):
  result = subprocess.run( \
    "pandoc --from=html --to=markdown+definition_lists --column=9999 --wrap=none", \
    shell=True, check=True, \
    capture_output=True, \
    input=html,text=True)

  md = []
  md_stack = []
  for line in result.stdout.split('\n'):
    if line == '::: jump-link' or line == '::: {.jump-link markdown="1"}':
      line = '{{<jump>}}'
      md_stack = [ 'jump' ] + md_stack
    elif line == '::: note' or line == '::: {.note markdown="1"}':
      line = '{{<note>}}'
      md_stack = [ 'note' ] + md_stack
    elif line == '::: {.info markdown="1"}':
      line = '{{<note info>}}'
      md_stack = [ 'note' ] + md_stack      
    elif line == '::: {.warn markdown="1"}':
      line = '{{<note warn>}}'
      md_stack = [ 'note' ] + md_stack      
    elif line == ':::':
      if md_stack:
        line = '{{</'+md_stack[0]+'>}}'
        md_stack = md_stack[1:]

    md.append(line)
  return '\n'.join(md)

def convertToMarkdown(html):
  moreText = '<!--more-->'

  parts = html.split(moreText)
  for i,p in enumerate(parts):
    parts[i] = htmlToMarkdown(p)
  print("# of parts: %d" % len(parts))
  return (moreText + '\n').join(parts)

def migrateToMarkdown(fname):
  if not(os.path.isfile(fname)):
    raise RuntimeError('File does not exist: %s' % fname)

  (file,ext) = os.path.splitext(fname)
  if ext != ".html":
    raise RuntimeError('File is not an HTML file: %s' % fname)

  (post,html) = common.read_blog_post(fname)

  if not(html):
    raise RuntimeError('Cannot get HTML text from %s' % fname)

  md = convertToMarkdown(html)

  common.set_series_tag(post)
  if 'title' in post:
    post['title'] = titlecase.titlecase(post['title'])

  ofile = "%s.md" % file
  with open(ofile,"wt") as output:
    output.write('---\n')
    output.write(yaml.dump(post,allow_unicode=True))
    output.write('---\n')
    output.write(md)
    output.close()
    return ofile

args = parseCLI()
for fname in args.files:
  ofile = migrateToMarkdown(fname)
  if ofile:
    print("Migrated to %s" % ofile)
    os.remove(fname)
