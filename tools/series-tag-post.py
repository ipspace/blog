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
  parser.add_argument('-c','--category', dest='category', action='store',help='Tag blog post if it has this category')
  parser.add_argument('-r','--remove', dest='remove', action='store',help='Remove category (tag) from blog post')
  parser.add_argument('-s','--series', dest='series', action='store',help='Tag blog post with this series')
  parser.add_argument('-t','--tag', dest='tag',action='store',help='Apply this intra-series tag')
  parser.add_argument('--log', dest='logging', action='store_true',help='Enable basic logging')
  parser.add_argument('-q','--quiet', dest='quiet', action='store_true',help='Be sparse with error messages')
  parser.add_argument('--verbose', dest='verbose', action='store_true',help='Enable more verbose logging')
  return parser.parse_args()

def series_tag_file(fname,args):
  if not(os.path.isfile(fname)):
    raise RuntimeError('File does not exist: %s' % fname)

  (file,ext) = os.path.splitext(fname)
  if ext != ".md" and not args.remove:
    raise RuntimeError('File is not an MD file: %s' % fname)

  (post,html) = common.read_blog_post(fname)

  if not(html):
    raise RuntimeError('Cannot get HTML text from %s' % fname)

  if not args.category and os.environ.get('BLOG_CATEGORY'):
    args.category = os.environ.get('BLOG_CATEGORY')

  if args.category:
    if not args.category in post.get('tags',[]):
      if not args.quiet:
        print(f'File {fname} not in category {args.category}, skipping')
        sys.exit(1)
      else:
        return None

  old_yaml = yaml.dump(post,allow_unicode=True)
  if args.remove:
    post['tags'] = [ t for t in post.get('tags',[]) if t != args.remove ]
  elif args.tag or args.series or args.category:
    common.set_series_tag(post,args.series or args.category,args.tag)
  else:
    print(f'Fatal: neither TAG nor REMOVE were set')
    sys.exit(1)

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
  if series_tag_file(fname,args):
    print(f"... tagged {fname}")
